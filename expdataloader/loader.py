from functools import cached_property
import os
from pathlib import Path
import traceback
from typing import Generic, TypeVar

from expdataloader.utils import FileLock, get_image_paths, get_sub_dir

BASE_DIR = Path(__file__).parent.parent / "data"
DATA_DIR = str(BASE_DIR)
TARGET_DIR = str(BASE_DIR / "target")
SOURCE_DIR = str(BASE_DIR / "source")


class InputData:
    def __init__(self, source_id: str, target_id: str):
        self.source_id = source_id
        self.target_id = target_id

    @cached_property
    def data_name(self):
        return f"{self.source_id}_{self.target_id}"

    @property
    def source_img_dir(self):
        return os.path.join(SOURCE_DIR, self.source_id)

    @cached_property
    def source_img_paths(self):
        return get_image_paths(self.source_img_dir)

    @property
    def source_img_path(self):
        return self.source_img_paths[0]

    @cached_property
    def target_dir(self):
        return os.path.join(TARGET_DIR, self.target_id)

    @cached_property
    def target_video_path(self):
        return os.path.join(self.target_dir, "face_crop.mp4")


class OutputData:
    def __init__(self, output_dir: str, data_name: str):
        self.output_dir = output_dir
        self.data_name = data_name

    @property
    def video_path(self):
        return os.path.join(self.output_dir, self.data_name + ".mp4")


class RowData:
    def __init__(self, input: InputData, output: OutputData):
        self.input = input
        self.output = output

    @property
    def data_name(self):
        return self.input.data_name

    @property
    def is_processed(self):
        return os.path.exists(self.output_video_path)

    @property
    def target_video_path(self):
        return self.input.target_video_path

    @property
    def source_img_path(self):
        return self.input.source_img_path

    @property
    def output_video_path(self):
        return self.output.video_path

    def __str__(self):
        return self.data_name


TROW = TypeVar("TROW", bound=RowData)


class HeadSwapDataLoader(Generic[TROW]):
    base_dir = os.path.join(DATA_DIR)

    def __init__(self, exp_name: str):
        self.exp_name = exp_name

    @cached_property
    def output_dir(self):
        return get_sub_dir(self.base_dir, "output", self.exp_name)

    def get_row(self, id: str) -> TROW:
        """
        id is the data_name of the row, e.g. "hsid_pid"
        """
        return self.all_data_rows_dict[id]

    @cached_property
    def lock_dir(self):
        return os.path.join(self.output_dir, "lock")

    def get_all_data_rows(self):
        for line in open(os.path.join(self.base_dir, "run_pair.txt")).readlines():
            pair = line.strip()
            if pair:
                hsid, pid = pair.split(" ")
                input = InputData(hsid, pid)
                output = OutputData(self.output_dir, input.data_name)
                yield RowData(input, output)

    @cached_property
    def all_data_rows_dict(self):
        return {row.data_name: row for row in self.all_data_rows}

    @cached_property
    def all_data_rows(self):
        return list(self.get_all_data_rows())

    def exp_data_row(self, row: TROW):
        lock_file = os.path.join(self.lock_dir, f"{row.data_name}.lock")
        with FileLock(lock_file) as lock:
            if not lock.acquire():
                print(f"Already running, skip: {row.data_name}")
                return

            if row.is_processed:
                print(f"Already processed, skip: {row.data_name}")
                return

            try:
                print(f"Running: {row}")
                self.run_video(row)
            except Exception as e:
                error_file_path = os.path.join(self.lock_dir, f"{row.data_name}.error")
                with open(error_file_path, "w") as f:
                    f.write(f"{e}\n")
                    traceback.print_exc(file=f)
                    traceback.print_exc()
                print(f"Error occurred: {e}. Logged to {error_file_path}")

    def run_video(self, row: TROW):
        raise NotImplementedError


class RowDataLoader(HeadSwapDataLoader[RowData]):
    all_exp_names = ["ours", "diffswap", "heser", "deeplivecam", "blendface", "faceapt", "infoswap"]
    pass

class CompLoader(RowDataLoader):
    def __init__(self, exp_name: str="comp"):
        super().__init__(exp_name)

    @cached_property
    def all_loaders(self):
        return [RowDataLoader(exp_name) for exp_name in self.all_exp_names]

    
def main():
    loader = CompLoader()
    for loader in loader.all_loaders:
        for row in loader.all_data_rows:
            if not os.path.exists(row.target_video_path):
                print(row.target_video_path)
            # if not row.is_processed:
            #     print(row.output_video_path)

if __name__ == "__main__":
    main()

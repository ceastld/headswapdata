from functools import cached_property

import numpy as np
from expdataloader import *
from expdataloader.utils import extract_frame, img_grid


class CompImageLoader(CompLoader):
    all_exp_names = ["ours", "diffswap", "heser", "deeplivecam", "blendface", "faceapt", "infoswap"]
    def __init__(self):
        super().__init__("comp_img")

    @cached_property
    def all_loaders(self):
        return [RowDataLoader(exp_name) for exp_name in self.all_exp_names]

    @cached_property
    def dataset(self):
        return [
            ("PID1", "HSID9", 0, 100),
            ("PID4", "HSID10", 2, 105),
            ("PID19", "HSID13", 0, 35),
            ("PID36", "HSID43", 0, 45),
        ]

    @cached_property
    def comp_img_dir(self):
        return os.path.join(self.output_dir, "comp_img1")

    def comp_img(self):
        img_paths = []

        for pid, hsid, source_id, frame_id in self.dataset:

            def append(video_path, img_path):
                img_path = extract_frame(video_path, frame_id, img_path)
                print(video_path, frame_id)
                img_paths.append(img_path)

            input = InputData(pid, hsid)
            source_img_path = input.source_img_paths[source_id]
            img_paths.append(source_img_path)

            target_dir = get_sub_dir(self.comp_img_dir, "1_target")
            append(input.target_video_path, os.path.join(target_dir, ))
            for loader in self.all_loaders:
                row = loader.get_row(input.data_name)
                append(row.output_video_path)
        save_path = "grid1.jpg"
        imgs = np.array(img_paths).reshape(len(self.dataset), -1)
        img_grid(imgs, save_path=save_path)


if __name__ == "__main__":
    CompImageLoader().comp_img()

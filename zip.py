import os
import zipfile
from expdataloader import *


def get_video_paths(video_dir):
    res = []
    for line in open("run_pair.txt").readlines():
        pair = line.strip()
        name = pair.replace(" ", "_")
        out_path = f"{video_dir}/{name}_{os.path.basename(video_dir)}.mp4"
        if os.path.exists(out_path):
            res.append(out_path)
        else:
            out_path = f"{video_dir}/{name}.mp4"
            if os.path.exists(out_path):
                res.append(out_path)
    return res


def compress_files_to_zip(file_paths, zip_file):
    try:
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in file_paths:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))
                else:
                    print(f"文件 {file} 不存在，跳过。")
        print(f"文件已成功压缩到 {zip_file}")
    except Exception as e:
        print(f"压缩时发生错误: {e}")


class Zip:
    def diffswap(self):
        video_paths = get_video_paths("diffswap")
        compress_files_to_zip(video_paths, "data/diffswap.zip")

    def heser(self):
        video_paths = get_video_paths("heser")
        compress_files_to_zip(video_paths, "data/heser.zip")

    def deeplivecam(self):
        video_paths = get_video_paths("deeplivecam")
        compress_files_to_zip(video_paths, "data/deeplivecam.zip")

    def faceapt(self):
        video_paths = get_video_paths("faceapt")
        compress_files_to_zip(video_paths, "data/face-adapter.zip")

    def blendface(self):
        video_paths = get_video_paths("blendface")
        compress_files_to_zip(video_paths, "data/blendface_unalign.zip")

if __name__ == "__main__":
    zip = Zip()
    zip.blendface()

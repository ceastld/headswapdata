import os
import subprocess

from natsort import natsorted


def get_pairs():
    res = []
    for line in open("exp_data/run_pair.txt").readlines():
        pair = line.strip()
        name = pair.replace(" ", "_")
        res.append(pair)
    return res


def crop_left_half(input_path, output_path):
    command = ["ffmpeg", "-i", input_path, "-vf", "crop=iw/2:ih:0:0", "-c:a", "copy", "-y", output_path]

    subprocess.run(command, check=True)


def get_video_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                image_paths.append(os.path.join(root, file))
    return natsorted(image_paths)


def exp_pair(pair):
    source_name = pair.split(" ")[0]  # PID
    target_name = pair.split(" ")[1]  # HSID
    name = pair.replace(" ", "_")


import re


def cut():
    dir = "exp_data/ours_sup"
    video_paths = get_video_paths(dir)
    for video_path in video_paths:
        name = str(os.path.basename(video_path))
        new_name = "_".join(re.split("_|\.", name)[1::-1]) + ".mp4"
        new_path = os.path.join(dir, new_name)
        crop_left_half(video_path, new_path)
        print(new_path)


if __name__ == "__main__":
    cut()

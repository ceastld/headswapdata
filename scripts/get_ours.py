import os
import shutil
import subprocess


def get_pairs():
    res = []
    for line in open("hanhai22/run_pair.txt").readlines():
        pair = line.strip()
        name = pair.replace(" ", "_")
        res.append(pair)
    return res


def crop_left_quarter(input_path, output_path):
    command = ["ffmpeg", "-i", input_path, "-vf", "crop=iw/4:ih:0:0", "-c:a", "copy", "-y", output_path]

    subprocess.run(command, check=True)


def exp_pair(pair: str, pre_eval_ids=[], exist_skip=True):
    source_name = pair.split(" ")[0]  # PID
    target_name = pair.split(" ")[1]  # HSID
    name = pair.replace(" ", "_")
    video_dir1 = f"hsoutput/{target_name}/{name}"
    if not os.path.isdir(video_dir1):
        video_dir1 = f"hsoutput/{target_name}/{source_name}"
        assert os.path.isdir(video_dir1), f"dont have any data: {name}"
    for idx in pre_eval_ids+list(range(500,0,-1)):
        ours_video_path = f"{video_dir1}/gaussian_scene_fea_dev/logs/{idx:04d}_eval.mp4"
        if os.path.exists(ours_video_path) and os.path.getsize(ours_video_path) > 10240:
            break
    
    target_dir = "hanhai22/ours_sup"
    os.makedirs(target_dir, exist_ok=True)
    target_video_path = f"{target_dir}/{name}.mp4"
    if exist_skip and os.path.exists(target_video_path):
        return
    crop_left_quarter(ours_video_path, target_video_path)
    # shutil.copy(ours_video_path, f"{target_dir}/{name}.mp4")


if __name__ == "__main__":
    pairs = get_pairs()
    # pairs = ["PID19 HSID13", "PID19 HSID35", "PID1 HSID9", "PID1 HSID24"]
    # exp_pair("PID36 HSID43", exist_skip=False)
    # exit()
    for pair in pairs:
        print(pair)
        if pair == "PID39 HSID2":
            exp_pair(pair, [10], exist_skip=True)
        else:
            exp_pair(pair, exist_skip=True)
            

import json
import os
import random
import shutil
import subprocess
import cv2
from natsort import natsorted
from expdataloader.utils import get_image_paths

def create_video_grid_with_labels(video_paths, image_path, output_path, labels=["1", "2", "3", "4"], fontsize=48):
    if len(video_paths) != 5:
        raise ValueError("视频路径列表必须包含5个视频路径。")

    # 获取第一个视频的宽高
    cap = cv2.VideoCapture(video_paths[0])
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    # 构造ffmpeg命令
    labels = ["target"] + labels + ["source"]
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # 可以根据需要更改字体路径

    # 为每个视频输入添加 -r 25 强制帧率为 25
    video_inputs = [f"-i {video_path} -r 25" for video_path in video_paths]
    video_inputs = " ".join(video_inputs)
    # fmt:off
    cmd = [
        'ffmpeg',
        *video_inputs.split(),
        '-i', image_path,
        '-filter_complex',
        f"""
        [5]scale={width}:{height}:force_original_aspect_ratio=decrease,
        pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black[img];
        [0]drawtext=text='{labels[0]}':x=10:y=10:fontsize={fontsize}:fontcolor=white:fontfile={font_path}[v0];
        [1]drawtext=text='{labels[1]}':x=10:y=10:fontsize={fontsize}:fontcolor=white:fontfile={font_path}[v1];
        [2]drawtext=text='{labels[2]}':x=10:y=10:fontsize={fontsize}:fontcolor=white:fontfile={font_path}[v2];
        [3]drawtext=text='{labels[3]}':x=10:y=10:fontsize={fontsize}:fontcolor=white:fontfile={font_path}[v3];
        [4]drawtext=text='{labels[4]}':x=10:y=10:fontsize={fontsize}:fontcolor=white:fontfile={font_path}[v4];
        [img]drawtext=text='{labels[5]}':x=10:y=10:fontsize={fontsize}:fontcolor=white:fontfile={font_path}[img_labeled];
        [v0][v1][v2]hstack=inputs=3[top];
        [img_labeled][v3][v4]hstack=inputs=3[bottom];
        [top][bottom]vstack=inputs=2[output]
        """,
        '-map', '[output]',
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'fast',
        '-shortest',
        '-frames:v', '1000',  # 限制最大帧数为1000
        '-y',
        output_path
    ]
    # fmt:on
    subprocess.run(cmd)


def get_pairs():
    res = []
    for line in open("run_pair.txt").readlines():
        pair = line.strip()
        name = pair.replace(" ", "_")
        out_path = f"heser/{name}_heser.mp4"
        if pair and os.path.exists(out_path) and not pair in res:
            res.append(pair)
    return res


def get_data(pair: str, shuffle=False):
    source_name = pair.split(" ")[0]  # PID
    target_name = pair.split(" ")[1]  # HSID
    source_img_path = get_image_paths(f"pids/{source_name}")[0]
    target_video_path = f"{target_name}/face_crop.mp4"
    name = pair.replace(" ", "_")

    diffswap_video = f"diffswap/{name}_diffswap.mp4"
    heser_video = f"heser_half/{name}_heser.mp4"
    deeplivecam_video = f"deeplivecam/{name}.mp4"
    # deeplivecam_video = f"heser_half/{name}_heser.mp4"  # test
    ours_video = f"ours_sup/{name}.mp4"
    # ours_video = f"heser_half/{name}_heser.mp4"  # test

    video_label_pair = [
        [deeplivecam_video, "deeplivecam"],
        [diffswap_video, "diffswap"],
        [ours_video, "ours"],
        [heser_video, "heser"],
    ]
    if shuffle:
        random.shuffle(video_label_pair)
    video_label_pair.insert(0, [target_video_path, "target"])
    output_path = f"{OUT_DIR_NAME}/{name}.mp4"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return (
        [a[0] for a in video_label_pair],  # video_path
        [f"{a[1]}" for i, a in enumerate(video_label_pair)],  # labels
        source_img_path,
        output_path,
    )


def test_merge():
    video_paths = ["diffswap/PID4_HSID10_diffswap.mp4"] * 5
    # 随机打乱
    img_path = "pids/PID4/0.jpg"
    create_video_grid_with_labels(video_paths, img_path, "test.mp4", 50)

def merge_study():
    random.seed(0)
    pairs = get_pairs()
    label_dict = {}
    exists_OK = False
    OUT_DIR_NAME = "comp_sup"
    for pair in pairs:
        video_paths, labels, img_path, out_video_path = get_data(pair, shuffle=False)
        if not (exists_OK and os.path.exists(out_video_path)):
            create_video_grid_with_labels(video_paths, img_path, out_video_path, labels=labels, fontsize=24)
            print(f"see {out_video_path}")
        label_dict[pair] = labels

    label_save_path = f"{OUT_DIR_NAME}/label.json"
    json.dump({key: label_dict[key] for key in natsorted(label_dict)}, open(label_save_path, "w"), indent=4)
    print(f"see {label_save_path}")

if __name__ == "__main__":
    random.seed(0)
    pairs = get_pairs()
    label_dict = {}
    exists_OK = False
    OUT_DIR_NAME = "comp_sup_one"
    root_dir = f"{OUT_DIR_NAME}"
    os.makedirs(root_dir, exist_ok=True)
    for pair in pairs:
        video_paths, labels, img_path, out_video_path = get_data(pair, shuffle=False)
        name = pair.replace(" ","_")
        save_dir = os.path.join(root_dir, name)
        os.makedirs(save_dir, exist_ok=True)
        shutil.copy(img_path, save_dir)
        for video_path, label in zip(video_paths, labels):
            save_path = os.path.join(save_dir, label+".mp4")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            shutil.copy(video_path, save_path)
            print(save_path)
        

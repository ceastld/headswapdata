import os
import shutil
from PIL import Image

def resize_and_crop(img, target_width, target_height):
    """
    将图像缩放并裁剪到指定大小，同时保持原始比例。

    参数:
        img (PIL.Image.Image): 要处理的图像。
        target_width (int): 目标宽度。
        target_height (int): 目标高度。

    返回:
        PIL.Image.Image: 已裁剪并缩放到目标大小的图像。
    """
    # 获取原始图像尺寸
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height
    target_ratio = target_width / target_height

    # 裁剪宽度或高度，使图像比例接近目标比例
    if aspect_ratio > target_ratio:
        # 原图太宽，需要裁剪宽度
        new_width = int(target_ratio * img_height)
        left = (img_width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img_height))
    elif aspect_ratio < target_ratio:
        # 原图太高，需要裁剪高度
        new_height = int(img_width / target_ratio)
        top = (img_height - new_height) // 2
        img = img.crop((0, top, img_width, top + new_height))

    # 缩放到目标尺寸
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    return img


def get_orinopro_dataset():
    return [
        ("PID1", "HSID9", [25, 50, 100]),
        ("PID19", "HSID13", [20, 0, 110]),
        ("PID66", "HSID28", [50, 150, 250]),
    ]


def cp_smplx_from_node11():
    dir = "hanhai22/body_track_orinopro"
    os.makedirs(dir, exist_ok=True)
    for pid, hsid, frames in get_orinopro_dataset():
        pth_path = f"houtput/{hsid}_{pid}_orinopro/gaussian/body_track/smplx_track.pth"
        target_path = f"{dir}/{pid}_{hsid}.pth"
        shutil.copy(pth_path, target_path)


def cp_orinopro_video():
    dir = "hanhai22/orinopro"
    os.makedirs(dir, exist_ok=True)
    for pid, hsid, frames in get_orinopro_dataset():
        video_path = f"houtput/{hsid}_{pid}_orinopro/gaussian/debug/for_training.mp4"
        target_path = f"{dir}/{pid}_{hsid}.mp4"
        shutil.copy(video_path, target_path)

def get_frames():
    dir = "hanhai22/orinopro/frames1"
    os.makedirs(dir,exist_ok=True)
    for pid,hsid,frames in get_orinopro_dataset():
        ori_img_dir = f"houtput/{hsid}_{pid}_orinopro/gaussian/ori_imgs"
        for frame in frames: 
            ori_img_path = f"{ori_img_dir}/{frame:06d}.jpg"
            target_path = f"{dir}/{pid}_{hsid}_{frame}.jpg"
            resize_and_crop(Image.open(ori_img_path),512,512).save(target_path)
            # shutil.copy(ori_img_path,target_path)
            print(target_path)

if __name__ == "__main__":
    # cp_smplx_from_node11()
    # cp_orinopro_video()
    get_frames()

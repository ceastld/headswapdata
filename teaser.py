import os
import numpy as np
from common import extract_few_frames, get_image_paths, img_grid, resize_and_crop
from PIL import Image


def get_teaser_dataset():
    return [
        ("PID19", "HSID13", [6, 7, 8], [20, 0, 110]),
        ("PID19", "HSID35", [3, 4, 5], [0, 50, 150]),
        ("PID1", "HSID9", [0, 1, 2], [30, 50, 100]),
        ("PID1", "HSID24", [4, 5, 3], [100, 80, 50]),
        ("PID66", "HSID28", [0, 2, 4], [245, 255, 260]),
        ("PID4", "HSID10", [0, 1, 2], [105, 110, 115]),
        ("PID8", "HSID2", [0, 1, 2], [10, 320, 325]),
        ("PID36", "HSID43", [0, 1, 2], [95, 100, 105]),
    ]


def get_teaser_imgs(with_info=False):
    dataset = get_teaser_dataset()
    img_paths = []
    info_all = []
    for pid, hsid, source_id, frame_ids in dataset:
        p = np.array(get_image_paths(f"pids/{pid}"))[source_id]
        res = []
        res.extend(p)
        info = []
        info.extend([f"{pid}_{s:02d}" for s in source_id])

        name = f"{pid}_{hsid}"

        def extend(video_path, label="v"):
            ps = extract_few_frames(video_path, frame_ids)
            print(video_path)
            res.extend(ps)
            info.extend([f"{name}_{label}_{f}" for f in frame_ids])

        extend(f"{hsid}/face_crop.mp4", label="target")
        extend(f"ours/{name}.mp4", label="ours")
        # extend(f"diffswap/{name}_diffswap.mp4")
        # extend(f"heser_half/{name}_heser.mp4")
        # extend(f"deeplivecam/{name}.mp4")
        img_paths.extend(np.array(res).reshape(-1, 3).T.flat)
        info_all.extend(np.array(info).reshape(-1, 3).T.flat)

    img_paths = np.array(img_paths).reshape(-1, 3).T
    info_all = np.array(info_all).reshape(-1, 3).T
    if with_info:
        return img_paths, info_all
    return img_paths


def teaser_save_1by1():
    imgs = get_teaser_imgs()
    save_dir = "teaser1"
    os.makedirs(save_dir, exist_ok=True)
    for i in range(0, imgs.shape[0]):
        for j in range(0, imgs.shape[1]):
            resize_and_crop(Image.open(imgs[i, j]), 512, 512).save(f"{save_dir}/{i:02d}_{j:02d}.jpg")


def tesaer_layout1():
    imgs = get_teaser_imgs()
    path = img_grid(imgs, save_path="teaser.jpg", vertical_margins=[0, 0, 10] * 5)
    os.system(f"code {path}")


def teaser_layout2():
    imgs = get_teaser_imgs()
    imgs1 = np.full((4, 7), "", dtype=object)
    imgs1[0, 0] = imgs[0, 0]
    imgs1[1, 0] = imgs[0, 1]
    imgs1[2, 0] = imgs[0, 6]
    imgs1[3, 0] = imgs[0, 7]
    imgs1[:2, 1:] = imgs[1:, :6]
    imgs1[2:, 1:] = imgs[1:, 6:]

    path = img_grid(imgs1, save_path="teaser.jpg", vertical_margins=[10] + [0, 0, 0] * 10, horizontal_margins=[0, 10, 0])
    os.system(f"code {path}")


def teaser_img_info():
    imgs, info_all = get_teaser_imgs(with_info=True)
    save_dir = "teaser"
    os.makedirs(save_dir, exist_ok=True)
    for img_path, info in zip(imgs.flat, info_all.flat):
        save_path = os.path.join(save_dir, info + ".jpg")
        resize_and_crop(Image.open(img_path), 512, 512).save(save_path)
        print(save_path)


def teaser_dir():
    imgs, infos = get_teaser_imgs(True)
    save_dir = "teaser2"
    os.makedirs(save_dir, exist_ok=True)
    for img_path, info in zip(imgs.flat, infos.flat):
        info_part = str(info).split("_")
        sub_path = "_".join(info_part[:-1]) + "/" + info_part[-1] + ".jpg"
        save_path = os.path.join(save_dir, sub_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        resize_and_crop(Image.open(img_path), 512, 512).save(save_path)
        print(save_path)


def get_smplx_img():
    dataset = [
        ("HSID9", [20]),
        ("HSID13", [20]),
        ("HSID28", [250]),
    ]
    os.makedirs("smplx", exist_ok=True)
    for hsid, frames in dataset:
        video_path = f"body_track/{hsid}_smplx.mp4"
        img_paths = extract_few_frames(video_path, frames)
        for img_path, frame in zip(img_paths, frames):
            save_path = f"smplx/{hsid}_{frame}.jpg"
            resize_and_crop(Image.open(img_path), 512, 512).save(save_path)
            print(save_path)


if __name__ == "__main__":
    # teaser_layout2()
    # teaser_save_1by1()
    # tesaer_layout1()
    # teaser_dir()
    # teaser_img_info()
    # get_smplx_img()
    teaser_img_info()

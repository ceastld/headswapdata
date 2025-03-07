import os
from expdataloader.utils import extract_few_frames, resize_and_crop
from PIL import Image

def get_orinopro_dataset():
    return [
        ("PID1", "HSID9", [25, 50, 100]),
        ("PID19", "HSID13", [20, 0, 110]),
        ("PID66", "HSID28", [50, 150, 250]),
    ]


def get_frames():
    dir = "orinopro_frames"
    os.makedirs(dir,exist_ok=True)
    for pid,hsid,frames in get_orinopro_dataset():
        video_path = f"orinopro/{pid}_{hsid}.mp4"
        img_paths = extract_few_frames(video_path, frames)
        for img_path,frame in zip(img_paths,frames): 
            target_path = f"{dir}/{pid}_{hsid}_{frame}.jpg"
            resize_and_crop(Image.open(img_path),512,512).save(target_path)
            print(target_path)

def get_smplx_img():
    dir = "orinopro/smplx"
    os.makedirs(dir, exist_ok=True)
    print("111")
    for pid, hsid, frames in get_orinopro_dataset():
        video_path = f"body_track_orinopro/{pid}_{hsid}_smplx.mp4"
        img_paths = extract_few_frames(video_path, frames)
        for img_path, frame in zip(img_paths, frames):
            save_path = f"{dir}/{pid}_{hsid}_{frame}.jpg"
            resize_and_crop(Image.open(img_path), 512, 512).save(save_path)
            print(save_path)

if __name__ == "__main__":
    # cp_smplx_from_node11()
    # cp_orinopro_video()
    # get_frames()
    get_smplx_img()

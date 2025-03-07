import numpy as np
import os

from expdataloader.utils import extract_few_frames, get_image_paths, img_grid


["source", "target", "diffswap", "heser", "deeplivecam", "ours", "blendface", "faceapt", "infoswap"]

dataset = [
    ("PID1", "HSID9", [0], [100]),
    # ("PID11", "HSID24",[10], [100]),
    ("PID4", "HSID10", [2], [105]),
    # ("PID4", "HSID10", [1], [110]),
    # ("PID4", "HSID10", [2], [115]),
    ("PID19", "HSID13", [0], [35]),
    # ("PID36", "HSID34",[0],[105]),
    # ("PID36", "HSID34",[0],[52]),
    ("PID36", "HSID34", [0], [45]),
]

img_paths = []

for pid, hsid, source_id, frame_ids in dataset:
    p = np.array(get_image_paths(f"pids/{pid}"))[source_id]
    img_paths.extend(p)
    name = f"{pid}_{hsid}"

    def extend(video_path):
        ps = extract_few_frames(video_path, frame_ids)
        print(video_path)
        img_paths.extend(ps)

    extend(f"{hsid}/face_crop.mp4")
    extend(f"ours/{name.replace('34','43')}.mp4")
    extend(f"diffswap/{name}_diffswap.mp4")
    extend(f"heser_half/{name}_heser.mp4")
    extend(f"deeplivecam/{name}.mp4")

comp_dir = "comp_img"
os.makedirs(comp_dir, exist_ok=True)
imgs = np.array(img_paths).reshape(-1, 6)
print(imgs.shape)
white = 0
path = img_grid(imgs, save_path="comparison_grid.jpg", vertical_margins=[white] * 10, horizontal_margins=[white] * 10)
os.system(f"code {path}")
exit()

for i in range(0, 4):
    img_grid(imgs[:1, 2 * i : 2 * i + 2], save_path=f"{comp_dir}/1_{i+1}.png")
    img_grid(imgs[1:, 2 * i : 2 * i + 2], save_path=f"{comp_dir}/2_{i+1}.png")

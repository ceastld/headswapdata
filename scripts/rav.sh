# python remove_anything_video.py \
#     --input_video ./data/video/WXID1.mp4 \
#     --coords_type key_in \
#     --point_coords 256 256 \
#     --point_labels 1 \
#     --dilate_kernel_size 15 \
#     --output_dir ./data/seg/WXID1/idx0 \
#     --sam_model_type "vit_t" \
#     --sam_ckpt ./weights/mobile_sam.pt \
#     --lama_config lama/configs/prediction/default.yaml \
#     --lama_ckpt ./pretrained_models/big-lama \
#     --tracker_ckpt vitb_384_mae_ce_32x4_ep300 \
#     --vi_ckpt ./pretrained_models/sttn.pth \
#     --mask_idx 0 \
#     --fps 25

python remove_anything_video1.py \
    --input_video ./data/HSID13/face_crop.mp4 \
    --coords_type key_in \
    --point_coords 640 360 \
    --point_labels 1 \
    --dilate_kernel_size 15 \
    --output_dir ./data/HSID13 \
    --sam_model_type "vit_h" \
    --sam_ckpt ./pretrained_models/sam_vit_h_4b8939.pth \
    --lama_config lama/configs/prediction/default.yaml \
    --lama_ckpt ./pretrained_models/big-lama \
    --tracker_ckpt vitb_384_mae_ce_32x4_ep300 \
    --vi_ckpt ./pretrained_models/sttn.pth \
    --mask_idx 0 \
    --fps 25

python remove_anything_video1.py \
    --input_video ./data/HSID6/face_crop.mp4 \
    --coords_type key_in \
    --point_coords 640 360 \
    --point_labels 1 \
    --dilate_kernel_size 15 \
    --output_dir ./data/HSID6 \
    --mask_idx 0 \
    --fps 25
ids=("2" "4" "5" "7" "8" "9" "10" "11" "14" "15" "17")  # 定义一个 id 列表

for id in "${ids[@]}"; do
    mkdir -p "hanhai22/HSID$id"
    # cp -r "output/HSID$id/gaussian/head_mask" "hanhai22/HSID$id"
    # cp -r "output/HSID$id/gaussian/seg_masks" "hanhai22/HSID$id"
    cp "output/HSID$id/gaussian/debug/face_crop.mp4" "hanhai22/HSID$id"
done

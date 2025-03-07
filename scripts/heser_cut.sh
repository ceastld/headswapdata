mkdir -p heser_half  # 创建输出文件夹 heser_half（如果不存在）

for video in heser/*.mp4; do
    filename=$(basename "$video")  # 获取文件名
    output="heser_half/$filename"  # 输出文件路径

    # 检查输出文件是否已经存在
    if [ -f "$output" ]; then
        echo "Skipping $filename as it already exists."
    else
        ffmpeg -i "$video" -vf "crop=in_w/2:in_h:in_w/2:0" -c:a copy "$output"
        echo "Processed $filename"
    fi
done

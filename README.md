# 头部交换实验

本项目包含了多个头部交换实验的代码和数据。

## 数据集结构

- `pids/`: 源图像目录,包含多个人物的头像图片
- `HSIDxx/`: 目标视频目录,包含多个人物的视频片段
- `run_pair.txt`: 记录了源图像和目标视频的配对关系

## 实验方法

包含以下几种头部交换方法的实现和结果:

- ours: 我们提出的方法
- diffswap: DiffSwap方法 
- heser: HeSeR方法
- deeplivecam: DeepLiveCam方法
- blendface: BlendFace方法
- faceapt: FaceAdapter方法
- infoswap: InfoSwap方法

## 工具说明

- `comp_img.py`: 生成对比图片
- `zip.py`: 压缩实验结果视频
- `orinopro.py`: 处理原始视频数据
- `expdataloader/`: 数据加载和处理工具

## 使用方法

1. 准备好源图像和目标视频数据
2. 在 run_pair.txt 中配置实验对
3. 运行相应方法的代码生成结果
4. 使用 comp_img.py 生成对比图片

import streamlit as st
import numpy as np
import os
import subprocess
import pkg_resources

import sys
from inference import main
installed_packages = pkg_resources.working_set
installed = [f"{pkg.key}=={pkg.version}" for pkg in installed_packages]


# 设置标题
st.title("嘴唇语音处理")

# 上传视频文件
uploaded_video = st.file_uploader("上传视频文件", type=["mp4", "avi", "mov"])
if uploaded_video is not None:
    # 保存上传的视频文件
    with open("video.mp4", "wb") as f:
        f.write(uploaded_video.getbuffer())
    st.success("视频文件已成功上传并保存为 video.mp4")

# 上传音频文件
uploaded_audio = st.file_uploader("上传音频文件", type=["mp3", "wav"])
if uploaded_audio is not None:
    # 保存上传的音频文件
    with open("audio.mp3", "wb") as f:
        f.write(uploaded_audio.getbuffer())
    st.success("音频文件已成功上传并保存为 audio.mp3")

# 设置命令和参数
command = [
    'python', 'inference.py',
    '--checkpoint_path', 'wav2lip_gan.pth',
    '--face', 'video.mp4',
    '--audio', 'audio.mp3'
]
# 当视频和音频文件都上传后，执行命令
if uploaded_video is not None and uploaded_audio is not None:
    with st.spinner("正在处理，请稍候..."):
        r# 模拟命令行参数
        sys.argv = ['inference.py', '--checkpoint_path', 'wav2lip_gan.pth', '--face', 'test.mp4', '--audio', '3s.mp3']

        # 调用 main 函数，它会像从命令行调用一样解析 sys.argv
        result = main()

    # 显示输出和错误信息
    if result.returncode == 0:
        st.success("处理完成！")
    else:
        st.error("处理失败，请检查输出信息。")
        st.text(result.stderr)
    st.success(installed)
    # 检查结果文件是否存在，并展示结果视频
    result_video_path = "results/result_voice.mp4"
    if os.path.exists(result_video_path):
        st.video(result_video_path)
    else:
        st.error("结果视频未生成，请检查代码和文件路径。")



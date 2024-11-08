import streamlit as st
import os
import sys
from inference import parse_args, main
import os
import subprocess


# 打印当前的 PATH 环境变量
st.text(f"当前 PATH: {os.environ['PATH']}")

# 假设 ffmpeg 位于项目的 'ffmpeg-7.1-full_build/bin' 路径下
ffmpeg_path = "/mount/src/lipwab/ffmpeg-7.1-full_build/bin"
# 输出当前工作目录和 ffmpeg 路径
st.text(f"当前工作目录: {os.getcwd()}")

st.text(f"ffmpeg 路径: {ffmpeg_path}")
st.text(f"ffmpeg 是否存在: {os.path.exists(ffmpeg_path)}")
# 动态添加 ffmpeg 路径到 PATH 环境变量
os.environ["PATH"] += os.pathsep + ffmpeg_path

# 打印更新后的 PATH
st.text(f"更新后的 PATH: {os.environ['PATH']}")




""" # 运行 ffmpeg 命令
try:
    result = subprocess.run(["/mount/src/lipwab/ffmpeg-7.1-full_build/bin/ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    st.success("ffmpeg 已成功运行！")
    st.text(result.stdout.decode())  # 打印输出
    st.text(result.stderr.decode())  # 打印错误输出（如果有的话）
except subprocess.CalledProcessError as e:
    st.error(f"ffmpeg 运行失败: {e}")
    st.text(e.stdout.decode())
    st.text(e.stderr.decode()) """

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



# 当视频和音频文件都上传后，执行命令
if uploaded_video is not None and uploaded_audio is not None:
    with st.spinner("正在处理，请稍候..."):
        # 模拟命令行参数
        sys.argv = ['inference.py', '--checkpoint_path', 'wav2lip_gan.pth', '--face', 'video.mp4', '--audio', 'audio.mp3']
        args = parse_args()
        # 调用 main 函数，它会像从命令行调用一样解析 sys.argv
        main(args)

    # 检查结果文件是否存在，并展示结果视频
    result_video_path = "results/result_voice.mp4"
    if os.path.exists(result_video_path):
        st.video(result_video_path)
    else:
        st.error("结果视频未生成，请检查代码和文件路径。")

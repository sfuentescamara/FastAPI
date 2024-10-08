# from app.dependencies import *
PROYECT_PATH = '/mnt/chromeos/GoogleDrive/MyDrive/github/fastAPI/fastapi_app/'

import ffmpeg
import cv2
import numpy as np
from yt_dlp import YoutubeDL
import os

def get_video_stream_url(youtube_url):
    ydl_opts = {
        'format': 'mp4',
        # 'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        # video_url = info_dict.get('url', None)
        return info_dict

def extract_frames(stream_url, output_folder, frame_interval=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # probe = ffmpeg.probe(stream_url)
    # video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(stream_url['width'])
    height = int(stream_url['height'])

    process = (
        ffmpeg
        .input(stream_url.get('url', None))
        # .input("/mnt/chromeos/GoogleDrive/MyDrive/github/fastAPI/fastapi_app/Dasha - Austin (Official Music Video) [FyjnbSsZ2tc].mp4")
        .filter('fps', fps=1/frame_interval)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True)
    )
    print(" ".join(process.args))

    frame_count = 0
    while True:
        in_bytes = process.stdout.read(width * height * 3)
        if not in_bytes:
            break
        frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        cv2.imwrite(os.path.join(output_folder, f'frame_{frame_count:04d}.jpg'), frame)
        frame_count += 1

    process.wait()
    print(f"Extracted {frame_count} frames")

# Usage
youtube_url = "https://www.youtube.com/watch?v=BaW_jenozKc"  # Replace with your YouTube video URL
youtube_url = "https://youtu.be/FyjnbSsZ2tc?si=SLwUuTEivy21vOjN"
output_path = PROYECT_PATH + "dwloads/"  # Current directory
output_folder = output_path + "frames/"
frame_interval = 1  # Extract one frame every second

stream_url = get_video_stream_url(youtube_url)
extract_frames(stream_url, output_folder, frame_interval)
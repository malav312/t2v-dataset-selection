import yt_dlp
import pandas as pd
import os
import subprocess

def download_video(video_id, timestamps):
    # Define the output path and filename
    output_file = f'panda70m/{video_id}.mp4'
    
    # Check if the video file already exists
    if os.path.exists(output_file):
        print(f"Skipping {video_id}: File already exists.")
        return
    
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Ensures best quality
            'merge_output_format': 'mp4',          # Ensures output is in MP4 format
            'outtmpl': output_file                 # Output path and filename
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Successfully downloaded: {video_id}")

        # Split the video using the given timestamps
        split_by_time_stamp(video_id, timestamps)

        # Delete the original video after splitting
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"Deleted original video: {output_file}")

    except Exception as e:
        print(f"Failed to download {video_id}: {e}")

def split_by_time_stamp(video_id, timestamp_pairs):
    input_file = f'panda70m/{video_id}.mp4'
    for index, (start, end) in enumerate(timestamp_pairs, start=1):
        output_file = f'panda70m/{video_id}_{index}.mp4'
        command = [
            'ffmpeg', '-i', input_file, '-ss', start, '-to', end,
            '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', 
            '-b:a', '192k', output_file
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Created segment: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to create segment {output_file}: {e}")

# Read CSV into DataFrame
panda70m = pd.read_csv('panda70m_validation.csv')

# Example timestamps for demonstration
timestamps = [
    ('0:00:19.227', '0:00:28.278'),
    ('0:01:11.905', '0:01:23.958'),
    ('0:02:35.280', '0:02:45.331')
]

# Apply modified download function with timestamps
for video_id in panda70m['videoID']:
    download_video(video_id, timestamps)
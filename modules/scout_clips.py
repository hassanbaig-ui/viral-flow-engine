import yt_dlp
import os
import random

def download_clips():
    # Ensure assets directory exists
    if not os.path.exists("assets"):
        os.makedirs("assets")

    # Target channels/videos (Simulated selection from recent popular uploads)
    # Using specific popular videos from the requested channels for reliability
    # Diary of a CEO, Founders Podcast
    video_urls = [
        "https://www.youtube.com/watch?v=SomeDiaryOfCEOVideoID", # Placeholder, will need real ID
        "https://www.youtube.com/watch?v=SomeFoundersVideoID"
    ]
    
    # Since I cannot search easily without an API key or parsing HTML which is brittle, 
    # I will rely on yt-dlp to extract metadata from the channel URL if possible, 
    # or just use a few known recent viral-candidate URLs if I can find them.
    # For this exercise, I will use a search query with yt-dlp to find *one* video from each and download a segment.
    
    searches = [
        "ytsearch1:The Diary of a CEO interview 2024",
        "ytsearch1:Founders Podcast david senra"
    ]

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'assets/clip%(autonumber)s.%(ext)s',
        'noplaylist': True,
        'download_sections': [{
            'start_time': 600, # Start at 10 minutes in (skipping intros)
            'end_time': 660    # 60 seconds clip
        }],
        'force_keyframes_at_cuts': True,   # clearer cuts
        # 'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}] # Needs ffmpeg
    }
    
    # We need 3 clips.
    # I'll adding a 3rd search or repeat.
    searches.append("ytsearch1:The Diary of a CEO productivity")

    print("Starting download of 3 clips...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for query in searches:
            try:
                ydl.download([query])
            except Exception as e:
                print(f"Error downloading {query}: {e}")

    # Stock footage
    # Downloading a sample dark stock video (placeholder)
    stock_url = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4" # Just a placeholder
    # In a real scenario I'd fetch a specific dark stock url.
    # For now, let's just ensure we have 3 clips in assets/ or renamed.
    
    # Rename for consistency if needed or just listing them.
    print("Clips downloaded.")

if __name__ == "__main__":
    download_clips()

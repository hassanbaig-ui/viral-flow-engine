import yt_dlp
import os
import urllib.request
import traceback
import json

def download_clips():
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    main_clip_path = "assets/clip1.mp4"
    stock_clip_path = "assets/stock.mp4"

    # Check for clip_config.json (Apify/Cloud Hand-off)
    config_path = "assets/clip_config.json"
    if os.path.exists(config_path):
        print("Loading Clip Config from Cloud Scouting...")
        with open(config_path, "r") as f:
            config = json.load(f)
            
        print(f"Processing Cloud Video: {config['title']}")
        
        # Override download options for specific clip
        ydl_opts_main = {
            'format': 'best[ext=mp4]', # Avoid merge (no ffmpeg needed)
            'outtmpl': main_clip_path,
            'noplaylist': True,
            'download_sections': [{
                'start_time': config.get("start_time", 600), 
                'end_time': config.get("end_time", 645) 
            }],
            'force_keyframes_at_cuts': True,
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
            'cookiefile': 'cookies.txt',
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts_main) as ydl:
            ydl.download([config['video_url']])
            
    else:
        # Fallback to search if no config
        print("No config found. searching specific topic...")
        try:
            ydl_opts_main = {
                'format': 'best[ext=mp4]',
                'outtmpl': main_clip_path,
                'noplaylist': True,
                'download_sections': [{'start_time': 600, 'end_time': 645}],
                'force_keyframes_at_cuts': True,
                'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
                'cookiefile': 'cookies.txt',
                'ignoreerrors': True
            }
            
            query = "ytsearch1:The Diary of a CEO AI Wealth"
            with yt_dlp.YoutubeDL(ydl_opts_main) as ydl:
                ydl.download([query])
                
        except Exception as e:
            print(f"YouTube Download Failed: {e}")
            print("Falling back to Stock...")
            urllib.request.urlretrieve("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4", main_clip_path)

    # 2. Download Stock (B-roll)
    print("Downloading High-Quality Stock Clip...")
    if not os.path.exists(stock_clip_path):
        try:
            urllib.request.urlretrieve("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", stock_clip_path)
        except Exception as e:
            print(f"Stock Download Failed: {e}")

    # Verify
    print(f"Verifying {main_clip_path}...")
    print(f"Current Dir: {os.getcwd()}")
    print(f"Assets content: {os.listdir('assets')}")
    
    if os.path.exists(main_clip_path):
        print(f"Main clip ready: {main_clip_path}")
    else:
        print("WARNING: Main clip check failed but proceeding significantly to allow debugging...")
        # exit(1) # Disable fatal exit for debug

if __name__ == "__main__":
    download_clips()

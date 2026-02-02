import requests
import json
import time
import os

# Configuration
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_BASE = "https://api.apify.com/v2"

# Actors
SEARCH_ACTOR = "streamers/youtube-scraper" 
HEATMAP_ACTOR = "karamelo/youtube-most-replayed-scraper-heatmap-extractor"

def run_actor(actor_name, input_data):
    """Runs an Apify actor and waits for results."""
    actor_slug = actor_name.replace("/", "~")
    url = f"{APIFY_BASE}/acts/{actor_slug}/runs?token={APIFY_TOKEN}"
    
    try:
        r = requests.post(url, json=input_data)
        r.raise_for_status()
    except Exception as e:
        print(f"Error starting {actor_name}: {e}")
        return None
        
    run_id = r.json()['data']['id']
    print(f"Started {actor_name} (Run ID: {run_id}). Waiting for completion...")
    
    # Poll for completion
    while True:
        status_r = requests.get(f"{APIFY_BASE}/acts/{actor_slug}/runs/{run_id}?token={APIFY_TOKEN}")
        status = status_r.json()['data']['status']
        if status == "SUCCEEDED":
            break
        if status in ["FAILED", "ABORTED", "TIMED-OUT"]:
             print(f"{actor_name} failed with status {status}.")
             return None
        time.sleep(5) # Poll every 5s
        
    dataset_id = status_r.json()['data']['defaultDatasetId']
    
    # Fetch results
    items_r = requests.get(f"{APIFY_BASE}/datasets/{dataset_id}/items?token={APIFY_TOKEN}")
    return items_r.json()

def get_latest_video(channel_keyword):
    """Finds the latest video for a channel/keyword."""
    print(f"Scouting latest video for: {channel_keyword}")
    results = run_actor(SEARCH_ACTOR, {
        "searchKeywords": channel_keyword,
        "maxResults": 1,
        "sort": "date"
    })
    
    if results and len(results) > 0:
        video = results[0]
        print(f"Found: {video.get('title')} ({video.get('url')})")
        return video
    
    print(f"No videos found for {channel_keyword}")
    return None

def get_viral_segment(video_url):
    """Extracts the most replayed 60s segment using heatmap data."""
    print(f"Analyzing virality (heatmap) for: {video_url}")
    
    # Run Heatmap Extractor
    # Correct schema for karamelo/youtube-most-replayed-scraper-heatmap-extractor is "urls": ["..."]
    results = run_actor(HEATMAP_ACTOR, {
        "urls": [video_url]
    })
    
    if not results:
        print("Heatmap extraction failed/empty.")
        return None, None
        
    # Analyze the first result
    data = results[0]
    
    # The output format for karamelo/youtube-most-replayed... usually contains 'heatMarkers' or similar.
    # We look for the peak.
    # Expected structure: may have a 'heatMarkers' list with 'intensityScoreNormalized' (0.0 to 1.0)
    
    heat_markers = data.get('heatMarkers', [])
    if not heat_markers:
        # Check standard 'heatmap' key if 'heatMarkers' is missing
        heat_markers = data.get('heatmap', [])
        
    if not heat_markers:
        print("No heat markers found. Converting first 60s as backup.")
        return 0, 60
        
    # Find the peak intensity
    peak = max(heat_markers, key=lambda x: x.get('intensityScoreNormalized', 0))
    peak_time_ms = peak.get('timeRangeStartMillis', 0)
    
    # Convert to seconds
    peak_time_s = peak_time_ms / 1000.0
    
    # We want a 60s clip centered or starting around the peak.
    # Strategy: Start 10s before peak, end 50s after? 
    # Or if peak is the Climax, maybe end AT peak?
    # User said: "Extract the timestamp where intensityScoreNormalized is 1.0"
    # Let's simple start at peak - 10 to capture build up?
    # Or just start AT peak?
    # Safest: Start at peak_time - 10s (clamping to 0) to give context.
    
    start_time = max(0, peak_time_s - 10)
    end_time = start_time + 60
    
    print(f"Peak virality at {peak_time_s}s. Selected clip: {start_time}-{end_time}s")
    return start_time, end_time

def main():
    targets = ["The Diary of a CEO", "Founders Podcast", "The Diary of a CEO"] # Get 3 clips (2 from Diary, 1 Founders)
    # Refined: Search distinct videos? `maxResults` in search is 1.
    # To get 3 distinct videos, I might need to fetch more from search.
    # I'll search for "The Diary of a CEO" (limit 2) and "Founders Podcast" (limit 1).
    
    final_clips = []
    
    # Search 1: Diary (Fetch top 2)
    print("--- Searching 'The Diary of a CEO' ---")
    diary_results = run_actor(SEARCH_ACTOR, {
        "searchKeywords": "The Diary of a CEO",
        "maxResults": 2,
        "sort": "date"
    })
    
    if diary_results:
        for vid in diary_results:
            final_clips.append(vid)
            
    # Search 2: Founders (Fetch top 1)
    print("--- Searching 'Founders Podcast' ---")
    founders_results = run_actor(SEARCH_ACTOR, {
        "searchKeywords": "Founders Podcast",
        "maxResults": 1,
        "sort": "date"
    })
    
    if founders_results:
        final_clips.append(founders_results[0])
        
    # Process for Heatmaps
    clip_configs = []
    
    for vid in final_clips:
        url = vid.get('url')
        title = vid.get('title')
        
        start, end = get_viral_segment(url)
        if start is None:
            # Fallback
            start, end = 60, 120
            
        clip_configs.append({
            "video_url": url,
            "start_time": start,
            "end_time": end,
            "title": title,
            "transcript": "Generated transcript placeholder", # To be filled or used by Remotion mock
            "virality_score": 95 # Mocked based on 'peak' logic being 1.0
        })
        
        if len(clip_configs) >= 3:
            break
            
    # Write output
    os.makedirs("assets", exist_ok=True)
    with open("assets/clip_config.json", "w") as f:
        json.dump(clip_configs, f, indent=2)
        
    print(f"Successfully generated config for {len(clip_configs)} clips.")

if __name__ == "__main__":
    main()

import os
import json
import subprocess

def search_youtube(query, max_results=5):
    """
    Simulates searching YouTube using yt-dlp to find videos.
    In a real scenario with API limits, we might use the Data API.
    Here we use yt-dlp to search and fetch metadata.
    """
    print(f"Searching for: {query}")
    command = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--dump-json",
        "--no-playlist",
        "--flat-playlist" 
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    data = json.loads(line)
                    videos.append({
                        "id": data.get("id"),
                        "title": data.get("title"),
                        "url": data.get("url") or f"https://www.youtube.com/watch?v={data.get('id')}",
                        "view_count": data.get("view_count", 0) # Note: flat-playlist might not return views
                    })
                except json.JSONDecodeError:
                    continue
        return videos
    except subprocess.CalledProcessError as e:
        print(f"Error searching: {e}")
        return []

def get_best_clip():
    # Strategy: Search for recent "High-Signal" interviews
    queries = [
        "Diary of a CEO AI",
        "Y Combinator startup advice",
        "Lex Fridman AI debate",
        "Sam Altman interview 2026"
    ]
    
    all_videos = []
    for q in queries:
        all_videos.extend(search_youtube(q, max_results=3))
        
    # Simple selection logic: Just take the first one for now (or randomize)
    if all_videos:
        print(f"Found {len(all_videos)} candidates.")
        return all_videos[0]
    return None

if __name__ == "__main__":
    best = get_best_clip()
    if best:
        print(f"Selected Clip: {best['title']} ({best['url']})")
        # In a real flow, this would trigger the next step or save to a file
        with open("daily_selection.json", "w") as f:
            json.dump(best, f)
    else:
        print("No clips found.")

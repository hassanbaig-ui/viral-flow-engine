import requests
import time
import os
import sys

# User must provide this via env var or input
API_KEY = os.getenv('AYRSHARE_API_KEY')

if not API_KEY:
    print("Error: AYRSHARE_API_KEY not found. Please set the environment variable.")
    # For testing/dev, user might input it or we wait.
    # We will exit if not found.
    # sys.exit(1)
    # Default placeholder to prevent immediate crash if user reads code
    API_KEY = "PLACEHOLDER_KEY" 

BASE_URL = "https://app.ayrshare.com/api"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Post Configuration
VIDEO_PATH = "remotion/out/video.mp4" # Assumption
VIDEO_URL = "https://github.com/hassanbaig-ui/viral-flow-engine/releases/download/v1/video.mp4" 
# NOTE: Ayrshare needs a public URL for video. 
# Since cloud render failed, we don't have a URL.
# I will use a placeholder URL for testing distribution logic.
# In production, this would be the artifact link from GitHub.
PLACEHOLDER_VIDEO = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"

POSTS = [
    {
        "platforms": ["tiktok"],
        "caption": "If you're not doing this, you're falling behind. 🛑 #viral #mindset #success #entrepreneur Link in bio 🔗",
        "mediaUrls": [PLACEHOLDER_VIDEO]
    },
    {
        "platforms": ["instagram"],
        "caption": "Success leaves clues. 🕵️‍♂️✨\n\nThe 1% don't just work harder—they think differently.\n\nChange your input to change your output. 👇\n\n#successmindset #wealthcreation #motivation",
        "mediaUrls": [PLACEHOLDER_VIDEO],
        "comment": "Drop a '🔥' if you're ready to level up!"
    },
    {
        "platforms": ["youtube"], # Shorts support via video type? Ayrshare handles it.
        "caption": "The 1% Secret to Success | Viral Motivation 🚀 #Shorts\n\nDiscover the hidden mindset shift. #motivation #wealth",
        "mediaUrls": [PLACEHOLDER_VIDEO]
    },
    {
        "platforms": ["twitter"],
        "caption": "Unpopular opinion: Hard work is NOT the key to wealth. Leverage is. 🧵 #wealth #leverage",
        "mediaUrls": [PLACEHOLDER_VIDEO]
    },
    {
        "platforms": ["facebook"],
        "caption": "This is the message everyone needs to hear today. 🙌\n\nTag a friend who needs this motivation! 💪",
        "mediaUrls": [PLACEHOLDER_VIDEO]
    }
]

def post_to_ayrshare(post_data):
    url = f"{BASE_URL}/post"
    # Basic post structure
    payload = {
        "post": post_data["caption"],
        "platforms": post_data["platforms"],
        "mediaUrls": post_data["mediaUrls"]
    }
    
    try:
        r = requests.post(url, headers=HEADERS, json=payload)
        response = r.json()
        if r.status_code == 200 and response.get("status") == "success":
            print(f"Success posting to {post_data['platforms']}: {response.get('sId') or response.get('id')}")
            return response.get("id") or response.get("refId")
        else:
            print(f"Failed to post to {post_data['platforms']}: {response}")
            return None
    except Exception as e:
        print(f"Error posting: {e}")
        return None

def add_comment(ref_id, comment, platform):
    if not ref_id: return
    # Ayrshare comment API (simplified structure)
    url = f"{BASE_URL}/comment"
    payload = {
        "id": ref_id,
        "comment": comment,
        "platforms": [platform]
    }
    try:
        r = requests.post(url, headers=HEADERS, json=payload)
        print(f"Comment added to {platform}: {r.json()}")
    except Exception as e:
        print(f"Error adding comment: {e}")

def main():
    print("Starting Staggered Distribution Strategy...")
    
    stagger_delay = 15 * 60 # 15 minutes
    # specific override for testing/demo: 5 seconds
    stagger_delay_demo = 5 
    
    for i, post in enumerate(POSTS):
        print(f"Processing Post {i+1}/{len(POSTS)} for {post['platforms']}...")
        
        ref_id = post_to_ayrshare(post)
        
        # Conversation Starter (Initial Comment)
        if "comment" in post and ref_id:
            print("Adding engagement comment...")
            time.sleep(2)
            add_comment(ref_id, post["comment"], post["platforms"][0])
            
        # Stagger logic
        if i < len(POSTS) - 1:
            print(f"Waiting {stagger_delay_demo}s before next post... (Demo Stagger)")
            time.sleep(stagger_delay_demo)

    print("Distribution Complete!")

if __name__ == "__main__":
    main()

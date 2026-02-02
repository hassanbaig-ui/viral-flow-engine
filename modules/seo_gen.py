import json
import random
import os

def generate_seo():
    print("Generating SEO Metadata...")
    
    if not os.path.exists("remotion/src/clip_config.json"):
        print("Config not found.")
        return

    with open("remotion/src/clip_config.json", "r") as f:
        clip_config = json.load(f)

    metadata = []
    
    # Templates
    titles = [
        "How to {topic} in 2026",
        "The Truth About {topic}",
        "Why {topic} is the Future",
        "{topic}: The 2026 Guide"
    ]
    
    hashtags_base = ["#AIWealth", "#Automation2026", "#WealthSecrets", "#FutureTech", "#Viral2026"]
    
    for clip in clip_config:
        topic = "Wealth" if "Wealth" in clip['title'] else "AI"
        
        # Title
        title = random.choice(titles).format(topic=topic)
        
        # Caption
        caption = f"Discover the secret to {topic} in this exclusive clip. The world is changing fast in 2026. Are you ready? 🚀 Pay attention to the details. This is how the 1% thinks. \n\nDouble tap if you agree! 👇\n\n"
        
        # Hashtags
        hashtags = " ".join(hashtags_base)
        
        metadata.append({
            "video_url": clip['video_url'], # Original YT URL
            "title": clip['title'],
            "seo_title": title,
            "caption": caption,
            "hashtags": hashtags,
            "affiliate_link": "https://example.com/affiliate/" + str(random.randint(1000, 9999))
        })
        
    os.makedirs("marketing", exist_ok=True)
    with open("marketing/post_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("SEO Metadata saved to marketing/post_metadata.json")

if __name__ == "__main__":
    generate_seo()

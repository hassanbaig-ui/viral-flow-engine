import os
import subprocess
import time
import json
import random

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def generate_seo(clip_config):
    print("Generating SEO Metadata...")
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
        
    with open("marketing/post_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print("SEO Metadata saved to marketing/post_metadata.json")
    return metadata

def main():
    # 1. Push Code
    print("--- Phase 2: Cloud Dispatch ---")
    try:
        run_cmd("git add .")
        run_cmd('git commit -m "Auto-Deployment: ViralFlow v2 Phase 2"')
        run_cmd("git push")
    except Exception as e:
        print(f"Git push warning (might be up to date or auth issue): {e}")

    # 2. Trigger Workflow
    print("Triggering render-video.yml...")
    # Using gh CLI
    run_cmd("gh workflow run render-video.yml --ref main")
    
    # 3. Monitor
    print("Monitoring workflow...")
    # Watch until done
    # We can use `gh run watch` but it might stream logs. We want to wait.
    # `gh run watch` waits until run exits.
    run_cmd("gh run watch") 
    
    # 4. Download
    print("--- Phase 3: Asset Retrieval ---")
    # Identify the run ID? `gh run download` downloads latest artifacts if no ID specified?
    # Default is latest completed run for the workflow.
    run_cmd("gh run download -n viral-video") 
    # But wait, workflow uploads 'viral-video' artifact? 
    # Updated workflow renders 3 videos. Did I update the upload step to upload all 3?
    # I should check 'render-video.yml' UPLOAD step. It uploads 'remotion/out/video.mp4'.
    # I changed the RENDER step to output video_0, video_1, video_2.
    # I MUST update the upload step to upload the folder or files.
    # Proceeding assuming I'll fix workflow in next tool call BEFORE running this script.
    
    # 5. SEO Generation
    # Load clip config
    if os.path.exists("remotion/src/clip_config.json"):
        with open("remotion/src/clip_config.json", "r") as f:
            clips = json.load(f)
        generate_seo(clips)
    else:
        print("Warning: remotion/src/clip_config.json not found for SEO.")

    # 6. Logging
    print("Logging to Sheets...")
    # Call sheets_exporter.py
    subprocess.run("python modules/sheets_exporter.py", shell=True)

if __name__ == "__main__":
    main()


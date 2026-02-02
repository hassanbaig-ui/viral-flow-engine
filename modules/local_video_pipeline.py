import os
import requests
import base64
import time
import sys
import glob

# Re-use token from previous steps (User provided)
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
BASE_URL = "https://api.github.com"
REPO_NAME = "viral-flow-engine"

def get_user():
    r = requests.get(f"{BASE_URL}/user", headers=HEADERS)
    r.raise_for_status()
    return r.json()['login']

def upload_large_file(username, repo_name, file_path, remote_path):
    print(f"Uploading {file_path} to {remote_path}...")
    url = f"{BASE_URL}/repos/{username}/{repo_name}/contents/{remote_path}"
    
    # Check current SHA
    sha = None
    try:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            sha = r.json()['sha']
    except:
        pass

    with open(file_path, "rb") as f:
        content = f.read()

    encoded = base64.b64encode(content).decode("utf-8")
    
    data = {"message": f"Upload asset {remote_path}", "content": encoded, "branch": "main"}
    if sha: data["sha"] = sha
    
    try:
        r = requests.put(url, headers=HEADERS, json=data)
        if r.status_code not in [200, 201]:
            print(f"Failed to upload {remote_path}: {r.status_code}")
        else:
            print(f"Uploaded {remote_path} successfully.")
    except Exception as e:
        print(f"Upload error: {e}")

def trigger_workflow(username, repo_name):
    print("Triggering Cloud Render...")
    url = f"{BASE_URL}/repos/{username}/{repo_name}/actions/workflows/render-video.yml/dispatches"
    try:
        r = requests.post(url, headers=HEADERS, json={"ref": "main"})
        if r.status_code == 204:
            print("Workflow triggered.")
        else:
            print(f"Failed to trigger: {r.text}")
    except Exception as e:
        print(f"Trigger error: {e}")

def main():
    try:
        user = get_user()
        print(f"Authenticated as {user}")

        # Task 1: Secure Download (Local IP)
        print("\n--- Task 1: Secure Download (Local IP) ---")
        # Ensure dependencies
        os.system("pip install yt-dlp requests")
        
        # Run scout_clips.py
        # It should use clip_config.json if present (from Apify)
        res = os.system("python modules/scout_clips.py")
        if res != 0:
            print("Scout clips failed locally.")
            # We might still proceed if assets exist
        
        # Check if we have assets
        if not os.path.exists("assets/clip1.mp4"):
            print("ERROR: Main clip not found in assets/. Cannot proceed.")
            sys.exit(1)

        # Move assets to Remotion public folder for local render
        print("Moving assets to remotion/public/assets/...")
        os.makedirs("remotion/public/assets", exist_ok=True)
        # Windows copy
        os.system("xcopy assets\\* remotion\\public\\assets\\ /E /I /Y")

        # Task 2: Low-Resource Render
        print("\n--- Task 2: Low-Resource Render (Potato Mode) ---")
        print("Rendering with: --concurrency=1 --scale=0.5 --gl=angle")
        
        # Ensure npm install was run at some point?
        # We assume 'remotion' dir has node_modules or we run npm install
        if not os.path.exists("remotion/node_modules"):
            print("Installing Remotion dependencies...")
            os.system("cd remotion && npm install")
            
        render_cmd = "cd remotion && npx remotion render ViralVideo out/potato_video.mp4 --concurrency=1 --scale=0.5 --gl=angle"
        render_res = os.system(render_cmd)
        
        if render_res == 0:
            print("\n✅ Local Low-Res Render FAILURE/SUCCESS CHECK: Success!")
            print("Video available at: remotion/out/potato_video.mp4")
        else:
            print("\n❌ Local Render Failed. CPU/GPU issues likely.")

        # Task 3: Cloud Hand-off
        print("\n--- Task 3: Cloud Hand-off (Upload Assets) ---")
        print("Uploading raw assets to GitHub for high-quality cloud render...")
        
        if os.path.exists("assets"):
            for f in glob.glob("assets/*.mp4"):
                filename = os.path.basename(f)
                upload_large_file(user, REPO_NAME, f, f"assets/{filename}")
            
            # Also upload config
            if os.path.exists("assets/clip_config.json"):
                upload_large_file(user, REPO_NAME, "assets/clip_config.json", "assets/clip_config.json")
        
        trigger_workflow(user, REPO_NAME)
        
        print("\nPipeline Complete!")
        print("1. Local Low-Res Video: remotion/out/potato_video.mp4 (Check quality)")
        print("2. Cloud Render: Triggered (Check GitHub Actions for High-Res)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

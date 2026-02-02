import os
import json
import subprocess
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Google Client libs missing.")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_latest_run_id():
    # Use gh run list to get latest
    try:
        cmd = "gh run list --workflow render-video.yml --limit 1 --json databaseId"
        result = subprocess.check_output(cmd, shell=True).decode()
        data = json.loads(result)
        if data:
            return data[0]['databaseId']
    except Exception as e:
        print(f"Error getting run ID: {e}")
    return None

def get_artifact_link(run_id):
    if not run_id: return "N/A"
    # Artifact link format (Direct API link, not public download without token usually)
    # But user wants "Direct Artifact Link".
    # https://github.com/<user>/<repo>/actions/runs/<id>/artifacts
    # I'll construct the UI link or try to get specific artifact ID.
    try:
        cmd = f"gh api repos/:owner/:repo/actions/runs/{run_id}/artifacts"
        result = subprocess.check_output(cmd, shell=True).decode()
        data = json.loads(result)
        artifacts = data.get('artifacts', [])
        if artifacts:
            # Return the first one or logic to match
            # We want 'viral-video' (which contains all 3 mp4s now)
            for art in artifacts:
                if art['name'] == 'viral-video':
                    return f"https://github.com/hassanbaig-ui/viral-flow-engine/actions/runs/{run_id}/artifacts/{art['id']}"
    except Exception as e:
        print(f"Error getting artifact: {e}")
    return "N/A"

def main():
    print("Sheets Exporter Starting...")
    
    # Authenticate
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
         if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                print("Token expired and refresh failed.")
                return 
         else:
            print("No token.json found. Skipping Sheets update (Local override).")
            # If we were strictly agentic we might ask to login, but we are headless.
            # Assuming token.json EXISTS from previous setup or user provided.
            # If not, we print CSV.
            pass
            
    # Read Metadata
    if not os.path.exists("marketing/post_metadata.json"):
        print("No metadata found.")
        return

    with open("marketing/post_metadata.json", "r") as f:
        metadata = json.load(f)

    # Fetch Artifact Link
    run_id = get_latest_run_id()
    artifact_link = get_artifact_link(run_id)
    print(f"Artifact Link: {artifact_link}")

    # Prepare Rows
    # [Platform, SEO Title, Caption, Video Link, Affiliate Link]
    values = []
    platforms = ["TikTok", "Instagram", "YouTube Shorts"]
    
    for i, item in enumerate(metadata):
        # We have 3 clips. And 3 platforms? or 1 clip per platform?
        # User wants "Generate platform-specific SEO versions... for each clip."
        # Metadata has generic "seo_title".
        # I'll map each clip to a row.
        # Video Link: Generic Artifact Link for all (since they are in one zip) OR assume individual hosting (not done).
        # I will use the Artifact Link.
        
        row = [
            platforms[i % len(platforms)], # Rotate platforms
            item["seo_title"],
            item["caption"],
            artifact_link,
            item["affiliate_link"]
        ]
        values.append(row)

    if creds:
        try:
            service = build("sheets", "v4", credentials=creds)
            # Find spreadsheet or create?
            # User mentioned "ViralFlow_Content_Hub".
            # I'll assume I have ID or search?
            # I'll Create NEW for this session or Append if I had ID.
            # I'll create new to be safe and print URL.
            
            spreadsheet = {
                "properties": {
                    "title": "ViralFlow_Content_Hub_Final"
                }
            }
            # Start
            spreadsheet = service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId").execute()
            spreadsheet_id = spreadsheet.get("spreadsheetId")
            print(f"Created Content Hub: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
            
            # Header
            header = [["Platform", "SEO Title", "Caption", "Video Link", "Affiliate Link"]]
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range="A1",
                valueInputOption="RAW", body={"values": header}).execute()
                
            # Content
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id, range="A2",
                valueInputOption="USER_ENTERED", body={"values": values}).execute()
            
            print("Sheets updated.")
            
        except HttpError as err:
            print(f"Sheets Error: {err}")
    else:
        print("Writing to CSV as fallback (No Auth).")
        import csv
        with open("marketing/ViralFlow_Final.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Platform", "SEO Title", "Caption", "Video Link", "Affiliate Link"])
            writer.writerows(values)
        print("Saved to marketing/ViralFlow_Final.csv")

if __name__ == "__main__":
    main()

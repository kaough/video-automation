import time
import os
import sys
from config import Config
from services.drive_service import DriveService
from services.ai_service import AIService
from services.youtube_service import YouTubeService
from services.sheets_service import SheetsService

def main():
    print("Starting Video Automation Workflow...")
    
    # Initialize Services
    try:
        drive_service = DriveService()
        ai_service = AIService()
        youtube_service = YouTubeService()
        sheets_service = SheetsService()
    except Exception as e:
        print(f"Failed to initialize services: {e}")
        return

    # Main Loop
    while True:
        try:
            print(f"Checking for new files in folder {Config.DRIVE_FOLDER_ID}...")
            new_files = drive_service.monitor_folder(Config.DRIVE_FOLDER_ID)
            
            if not new_files:
                print("No new files found. Waiting...")
                time.sleep(60) # Check every minute
                continue

            for file in new_files:
                print(f"Processing file: {file['name']} (ID: {file['id']})")
                process_file(file, drive_service, ai_service, youtube_service, sheets_service)
                
                # For this MVP, we might want to stop after one file or mark it as processed.
                # Since we don't have a database, we'll just sleep for a bit to avoid re-processing immediately
                # In a real app, we'd move the file or store its ID.
                # For now, let's assume the user removes the file or we just wait a long time.
                print("File processed. Waiting before next check...")
                time.sleep(60)

        except KeyboardInterrupt:
            print("Stopping workflow...")
            break
        except Exception as e:
            print(f"Global error: {e}")
            time.sleep(60)

def process_file(file, drive_service, ai_service, youtube_service, sheets_service):
    retries = Config.MAX_RETRIES
    for attempt in range(retries + 1):
        try:
            # 1. Download Video
            video_path = os.path.join(os.getcwd(), file['name'])
            print(f"Downloading {file['name']}...")
            drive_service.download_file(file['id'], video_path)
            
            # 2. Analyze Video
            print("Analyzing video...")
            analysis = ai_service.analyze_video(video_path)
            title = analysis.get('title', 'Untitled Video')
            description = analysis.get('description', 'No description.')
            thumbnail_prompt = analysis.get('thumbnail_prompt', 'A cool video thumbnail')
            
            # 3. Generate Thumbnail
            print("Generating thumbnail...")
            thumbnail_path = os.path.join(os.getcwd(), 'thumbnail.png')
            ai_service.generate_thumbnail(thumbnail_prompt, thumbnail_path, title=title)
            # thumbnail_path = None
            
            # 4. Upload to YouTube (both accounts if enabled)
            print("Uploading to YouTube...")
            video_ids = youtube_service.upload_to_both_accounts(video_path, title, description, thumbnail_path)
            
            # Build YouTube links
            youtube_links = []
            if video_ids.get('primary'):
                youtube_links.append(f"Primary: https://youtu.be/{video_ids['primary']}")
            if video_ids.get('secondary'):
                youtube_links.append(f"Secondary: https://youtu.be/{video_ids['secondary']}")
            
            youtube_link = " | ".join(youtube_links) if youtube_links else "Upload failed"
            
            # 5. Log to Sheets
            print("Logging to Sheets...")
            sheets_service.log_run(file['name'], title, description, youtube_link)
            
            # 6. Confirmation
            print("\n" + "="*30)
            print("SUCCESS! Video Uploaded.")
            print(f"Title: {title}")
            print(f"Links: {youtube_link}")
            print(f"Summary: {description[:100]}...")
            print("="*30 + "\n")
            
            # 7. Move to Done Folder
            if Config.DRIVE_DONE_FOLDER_ID and Config.DRIVE_DONE_FOLDER_ID != 'YOUR_DONE_FOLDER_ID_HERE':
                print(f"Moving file to Done folder ({Config.DRIVE_DONE_FOLDER_ID})...")
                drive_service.move_file_to_folder(file['id'], Config.DRIVE_DONE_FOLDER_ID)
            else:
                print("No Done folder configured. Skipping move.")
            
            # Cleanup
            if os.path.exists(video_path):
                os.remove(video_path)
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                
            return # Success

        except Exception as e:
            print(f"Error processing file (Attempt {attempt + 1}/{retries + 1}): {e}")
            if attempt < retries:
                time.sleep(Config.RETRY_DELAY_SECONDS)
            else:
                print("Max retries reached. Skipping file.")
                # Send error notification (console for now)
                print(f"FAILED to process {file['name']}. Please check logs.")

if __name__ == "__main__":
    main()

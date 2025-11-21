"""
Debug script to check what files are in your Google Drive folder
"""
from services.drive_service import DriveService
from config import Config

def check_files():
    print("Connecting to Google Drive...")
    drive_service = DriveService()
    
    print(f"\nChecking folder ID: {Config.DRIVE_FOLDER_ID}")
    print("="*60)
    
    # Get ALL files in the folder (not just video files)
    query = f"'{Config.DRIVE_FOLDER_ID}' in parents and trashed = false"
    results = drive_service.service.files().list(
        q=query, 
        pageSize=50, 
        fields="nextPageToken, files(id, name, createdTime, mimeType)"
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print("❌ NO FILES FOUND in this folder!")
        print("\nPossible issues:")
        print("1. The folder ID might be wrong")
        print("2. The files might be in a different folder")
        print("3. The files might have been moved to the Done folder")
    else:
        print(f"✓ Found {len(items)} file(s) in the folder:\n")
        
        video_count = 0
        for item in items:
            name = item['name']
            mime_type = item.get('mimeType', 'unknown')
            file_id = item['id']
            
            # Check if it's a video file
            is_video = any(name.lower().endswith(ext) for ext in Config.VIDEO_EXTENSIONS)
            
            if is_video:
                video_count += 1
                print(f"✓ VIDEO: {name}")
            else:
                print(f"  (skip): {name}")
            
            print(f"    Type: {mime_type}")
            print(f"    ID: {file_id}\n")
        
        print("="*60)
        print(f"Summary: {video_count} video file(s), {len(items) - video_count} other file(s)")
        print(f"\nSupported video extensions: {Config.VIDEO_EXTENSIONS}")
        
        if video_count == 0:
            print("\n⚠️  No video files found!")
            print("Make sure your files have one of these extensions:")
            for ext in Config.VIDEO_EXTENSIONS:
                print(f"  - {ext}")

if __name__ == "__main__":
    try:
        check_files()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

import os

class Config:
    # Google Cloud Credentials
    CREDENTIALS_FILE = os.environ.get('CREDENTIALS_FILE', 'credentials.json')
    TOKEN_FILE = os.environ.get('TOKEN_FILE', 'token.json')
    
    # Drive Settings
    # The ID of the folder to monitor. 
    # You can find this in the URL of the folder in Google Drive: drive.google.com/drive/folders/<FOLDER_ID>
    DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID', 'YOUR_DRIVE_FOLDER_ID_HERE')
    DRIVE_DONE_FOLDER_ID = os.environ.get('DRIVE_DONE_FOLDER_ID', 'YOUR_DONE_FOLDER_ID_HERE')
    
    # Gemini AI Settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
    
    # OpenAI Settings (for DALL-E 3 thumbnail generation)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY_HERE')
    
    # YouTube Settings
    YOUTUBE_PRIVACY_STATUS = 'public'
    YOUTUBE_CATEGORY_ID = '22' # People & Blogs
    
    # Sheets Settings
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', 'YOUR_SPREADSHEET_ID_HERE')
    
    # Retry Settings
    MAX_RETRIES = 2
    RETRY_DELAY_SECONDS = 5

    # Supported Video Extensions
    VIDEO_EXTENSIONS = ('.mp4', '.mov', '.m4v')

    # Global Scopes
    SCOPES = [
        'https://www.googleapis.com/auth/drive', # Full access to move files
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/spreadsheets'
    ]

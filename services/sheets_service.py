import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import Config
import datetime

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsService:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)

    def _authenticate(self):
        creds = None
        if os.path.exists(Config.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(Config.TOKEN_FILE, Config.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(Config.CREDENTIALS_FILE):
                     flow = InstalledAppFlow.from_client_secrets_file(
                        Config.CREDENTIALS_FILE, Config.SCOPES)
                     creds = flow.run_local_server(port=0)
                else:
                    raise FileNotFoundError(f"Credentials file {Config.CREDENTIALS_FILE} not found.")
            with open(Config.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return creds

    def log_run(self, video_file, title, description, youtube_link):
        values = [
            [
                datetime.datetime.now().isoformat(),
                video_file,
                title,
                description,
                youtube_link
            ]
        ]
        body = {
            'values': values
        }
        
        print(f"Logging to Sheet {Config.SPREADSHEET_ID}...")
        result = self.service.spreadsheets().values().append(
            spreadsheetId=Config.SPREADSHEET_ID,
            range="Sheet1!A:E",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        
        print(f"{result.get('updates').get('updatedCells')} cells updated.")

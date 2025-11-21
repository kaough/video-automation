import os
import io
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from config import Config

# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveService:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)

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

    def monitor_folder(self, folder_id):
        """
        Checks for new files in the specified folder.
        This is a simplified version that checks for files created after a certain time 
        or just lists recent files. For a robust trigger, we'd need to store state.
        For this MVP, we'll list files that match the criteria.
        """
        query = f"'{folder_id}' in parents and trashed = false"
        results = self.service.files().list(
            q=query, pageSize=10, fields="nextPageToken, files(id, name, createdTime, mimeType)").execute()
        items = results.get('files', [])
        
        valid_files = []
        for item in items:
            name = item['name']
            if any(name.lower().endswith(ext) for ext in Config.VIDEO_EXTENSIONS):
                valid_files.append(item)
        
        return valid_files

    def download_file(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_name, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print(f"Download {int(status.progress() * 100)}%.")
        return file_name

    def move_file_to_folder(self, file_id, target_folder_id):
        """
        Moves a file to a new folder by adding the new parent and removing the old one.
        """
        # Retrieve the existing parents to remove
        file = self.service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        
        # Move the file by adding the new parent and removing the old parents
        self.service.files().update(
            fileId=file_id,
            addParents=target_folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        print(f"Moved file {file_id} to folder {target_folder_id}")

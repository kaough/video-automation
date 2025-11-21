import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import Config

class YouTubeService:
    def __init__(self, credentials_file=None, token_file=None):
        """
        Initialize YouTube service with optional custom credentials.
        If not provided, uses default from Config.
        """
        self.credentials_file = credentials_file or Config.CREDENTIALS_FILE
        self.token_file = token_file or Config.TOKEN_FILE
        self.creds = self._authenticate()
        self.service = build('youtube', 'v3', credentials=self.creds)

    def _authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, Config.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(self.credentials_file):
                     flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, Config.SCOPES)
                     creds = flow.run_local_server(port=0)
                else:
                    raise FileNotFoundError(f"Credentials file {self.credentials_file} not found.")
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        return creds

    def upload_video(self, file_path, title, description, thumbnail_path=None):
        """Upload video to YouTube"""
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': Config.YOUTUBE_CATEGORY_ID
            },
            'status': {
                'privacyStatus': Config.YOUTUBE_PRIVACY_STATUS,
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        
        print(f"Uploading {file_path} to YouTube...")
        request = self.service.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        video_id = response.get('id')
        print(f"Upload Complete! Video ID: {video_id}")

        if thumbnail_path and os.path.exists(thumbnail_path):
            print(f"Uploading thumbnail...")
            self.service.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            
        return video_id

    @staticmethod
    def upload_to_both_accounts(file_path, title, description, thumbnail_path=None):
        """
        Upload video to both YouTube accounts.
        Returns dict with both video IDs.
        """
        results = {}
        
        # Check if dual upload is enabled
        if not hasattr(Config, 'ENABLE_DUAL_UPLOAD') or not Config.ENABLE_DUAL_UPLOAD:
            # Single upload only
            service = YouTubeService()
            video_id = service.upload_video(file_path, title, description, thumbnail_path)
            results['primary'] = video_id
            return results
        
        # Upload to primary account
        print("\n=== Uploading to PRIMARY YouTube account ===")
        try:
            primary_service = YouTubeService()
            primary_id = primary_service.upload_video(file_path, title, description, thumbnail_path)
            results['primary'] = primary_id
            print(f"✓ Primary upload successful: https://youtu.be/{primary_id}")
        except Exception as e:
            print(f"✗ Primary upload failed: {e}")
            results['primary'] = None
        
        # Upload to secondary account
        print("\n=== Uploading to SECONDARY YouTube account ===")
        try:
            if not os.path.exists(Config.SECOND_CREDENTIALS_FILE):
                print(f"Warning: {Config.SECOND_CREDENTIALS_FILE} not found. Skipping secondary upload.")
                results['secondary'] = None
            else:
                secondary_service = YouTubeService(
                    credentials_file=Config.SECOND_CREDENTIALS_FILE,
                    token_file=Config.SECOND_TOKEN_FILE
                )
                secondary_id = secondary_service.upload_video(file_path, title, description, thumbnail_path)
                results['secondary'] = secondary_id
                print(f"✓ Secondary upload successful: https://youtu.be/{secondary_id}")
        except Exception as e:
            print(f"✗ Secondary upload failed: {e}")
            results['secondary'] = None
        
        return results

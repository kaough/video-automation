"""
Authentication helper for SECOND YouTube account.
Run this to authenticate kocvisuals@gmail.com
"""
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import Config

def authenticate_second():
    """Authenticate second account and save credentials"""
    creds = None
    
    # Check if token already exists
    if os.path.exists(Config.SECOND_TOKEN_FILE):
        print(f"Found existing token file: {Config.SECOND_TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(Config.SECOND_TOKEN_FILE, Config.SCOPES)
    
    # If credentials are invalid or don't exist, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow for SECOND account...")
            print(f"Using credentials file: {Config.SECOND_CREDENTIALS_FILE}")
            
            if not os.path.exists(Config.SECOND_CREDENTIALS_FILE):
                raise FileNotFoundError(f"Credentials file not found: {Config.SECOND_CREDENTIALS_FILE}")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.SECOND_CREDENTIALS_FILE, 
                Config.SCOPES
            )
            
            # This will open a browser window automatically
            print("\n" + "="*60)
            print("A browser window will open for authentication.")
            print("Please sign in with: kocvisuals@gmail.com")
            print("IMPORTANT: Make sure this email is added as a test user!")
            print("="*60 + "\n")
            
            creds = flow.run_local_server(port=8081)
        
        # Save the credentials
        with open(Config.SECOND_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"\n✓ Authentication successful! Token saved to: {Config.SECOND_TOKEN_FILE}")
    else:
        print("✓ Valid credentials already exist!")
    
    return creds

if __name__ == "__main__":
    try:
        authenticate_second()
        print("\n" + "="*60)
        print("SUCCESS! Second account authenticated.")
        print("You can now run: python main.py")
        print("Videos will upload to BOTH YouTube accounts!")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials_second.json exists")
        print("2. Make sure kocvisuals@gmail.com is added as a test user")
        print("3. Go to Google Cloud Console → OAuth consent screen → Test users")

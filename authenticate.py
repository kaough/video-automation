"""
Simple authentication helper script.
Run this to authenticate your Google account.
"""
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import Config

def authenticate():
    """Authenticate and save credentials"""
    creds = None
    
    # Check if token already exists
    if os.path.exists(Config.TOKEN_FILE):
        print(f"Found existing token file: {Config.TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(Config.TOKEN_FILE, Config.SCOPES)
    
    # If credentials are invalid or don't exist, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print(f"Using credentials file: {Config.CREDENTIALS_FILE}")
            
            if not os.path.exists(Config.CREDENTIALS_FILE):
                raise FileNotFoundError(f"Credentials file not found: {Config.CREDENTIALS_FILE}")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.CREDENTIALS_FILE, 
                Config.SCOPES
            )
            
            # This will open a browser window automatically
            print("\n" + "="*60)
            print("A browser window will open for authentication.")
            print("Please sign in with: kocvisuals@gmail.com")
            print("="*60 + "\n")
            
            creds = flow.run_local_server(port=8080)
        
        # Save the credentials
        with open(Config.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"\n✓ Authentication successful! Token saved to: {Config.TOKEN_FILE}")
    else:
        print("✓ Valid credentials already exist!")
    
    return creds

if __name__ == "__main__":
    try:
        authenticate()
        print("\n" + "="*60)
        print("SUCCESS! You can now run: python main.py")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials.json exists in the project folder")
        print("2. Make sure you added kocvisuals@gmail.com as a test user")
        print("3. Try running this script again")

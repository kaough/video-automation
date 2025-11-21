"""
Interactive Setup Wizard for Video Automation
Guides users through the complete configuration process
"""
import os
import sys
import json
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def get_input(prompt, default=None, required=True):
    """Get user input with optional default value"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        
        if not value and default:
            return default
        
        if not value and required:
            print_error("This field is required. Please enter a value.")
            continue
        
        return value

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 12:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python 3.12+ required. You have {version.major}.{version.minor}.{version.micro}")
        print_info("Please upgrade Python: https://www.python.org/downloads/")
        return False

def check_credentials_file():
    """Check if credentials.json exists"""
    print_header("Checking OAuth Credentials")
    
    if os.path.exists('credentials.json'):
        print_success("credentials.json found")
        
        # Validate it's valid JSON
        try:
            with open('credentials.json', 'r') as f:
                data = json.load(f)
                if 'installed' in data or 'web' in data:
                    print_success("credentials.json appears valid")
                    return True
                else:
                    print_error("credentials.json doesn't appear to be an OAuth credential file")
                    return False
        except json.JSONDecodeError:
            print_error("credentials.json is not valid JSON")
            return False
    else:
        print_error("credentials.json not found")
        print_info("Please download OAuth credentials from Google Cloud Console")
        print_info("See SETUP.md Step 3.3 for instructions")
        return False

def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt not found")
        return False
    
    print_info("Installing packages from requirements.txt...")
    result = os.system(f"{sys.executable} -m pip install -r requirements.txt -q")
    
    if result == 0:
        print_success("All dependencies installed successfully")
        return True
    else:
        print_error("Failed to install dependencies")
        return False

def create_config():
    """Interactive configuration creation"""
    print_header("Configuration Setup")
    
    print_info("Let's set up your configuration. You'll need:")
    print("  • Google Drive folder IDs (2)")
    print("  • Google Gemini API key")
    print("  • OpenAI API key")
    print("  • Google Sheets spreadsheet ID")
    print()
    
    # Get configuration values
    config_values = {}
    
    print(f"\n{Colors.BOLD}Google Drive Settings{Colors.END}")
    print_info("Find folder IDs in the URL: drive.google.com/drive/folders/FOLDER_ID")
    config_values['DRIVE_FOLDER_ID'] = get_input("Folder ID to monitor (Videos to Process)")
    config_values['DRIVE_DONE_FOLDER_ID'] = get_input("Done folder ID (processed videos)")
    
    print(f"\n{Colors.BOLD}AI API Keys{Colors.END}")
    config_values['GEMINI_API_KEY'] = get_input("Google Gemini API key")
    config_values['OPENAI_API_KEY'] = get_input("OpenAI API key (for DALL-E 3)")
    
    print(f"\n{Colors.BOLD}Google Sheets Settings{Colors.END}")
    print_info("Find spreadsheet ID in the URL: docs.google.com/spreadsheets/d/SPREADSHEET_ID")
    config_values['SPREADSHEET_ID'] = get_input("Google Sheets spreadsheet ID")
    
    print(f"\n{Colors.BOLD}YouTube Settings{Colors.END}")
    privacy = get_input("Default privacy status", default="public")
    category = get_input("YouTube category ID", default="22")
    
    config_values['YOUTUBE_PRIVACY_STATUS'] = privacy
    config_values['YOUTUBE_CATEGORY_ID'] = category
    
    # Optional: Dual upload
    print(f"\n{Colors.BOLD}Advanced: Dual YouTube Upload (Optional){Colors.END}")
    dual_upload = get_input("Enable dual account upload? (yes/no)", default="no", required=False)
    
    if dual_upload.lower() in ['yes', 'y']:
        config_values['ENABLE_DUAL_UPLOAD'] = True
        config_values['SECOND_CREDENTIALS_FILE'] = 'credentials_second.json'
        config_values['SECOND_TOKEN_FILE'] = 'token_second.json'
        print_warning("You'll need to create credentials_second.json separately")
    else:
        config_values['ENABLE_DUAL_UPLOAD'] = False
    
    # Write config.py
    config_content = f'''import os

class Config:
    # Google Cloud Credentials
    CREDENTIALS_FILE = os.environ.get('CREDENTIALS_FILE', 'credentials.json')
    TOKEN_FILE = os.environ.get('TOKEN_FILE', 'token.json')
    
    # Drive Settings
    DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID', '{config_values['DRIVE_FOLDER_ID']}')
    DRIVE_DONE_FOLDER_ID = os.environ.get('DRIVE_DONE_FOLDER_ID', '{config_values['DRIVE_DONE_FOLDER_ID']}')
    
    # Gemini AI Settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '{config_values['GEMINI_API_KEY']}')
    
    # OpenAI Settings (for DALL-E 3 thumbnail generation)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '{config_values['OPENAI_API_KEY']}')
    
    # YouTube Settings
    YOUTUBE_PRIVACY_STATUS = '{config_values['YOUTUBE_PRIVACY_STATUS']}'
    YOUTUBE_CATEGORY_ID = '{config_values['YOUTUBE_CATEGORY_ID']}'
    
    # Sheets Settings
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '{config_values['SPREADSHEET_ID']}')
    
    # Retry Settings
    MAX_RETRIES = 2
    RETRY_DELAY_SECONDS = 5

    # Supported Video Extensions
    VIDEO_EXTENSIONS = ('.mp4', '.mov', '.m4v')

    # Global Scopes
    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
'''
    
    if config_values['ENABLE_DUAL_UPLOAD']:
        config_content += f'''
    # Dual Upload Settings
    ENABLE_DUAL_UPLOAD = True
    SECOND_CREDENTIALS_FILE = '{config_values['SECOND_CREDENTIALS_FILE']}'
    SECOND_TOKEN_FILE = '{config_values['SECOND_TOKEN_FILE']}'
'''
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print_success("config.py created successfully")
    return True

def run_authentication():
    """Run the authentication script"""
    print_header("Google Authentication")
    
    print_info("Running authentication script...")
    print_info("A browser window will open. Please sign in and grant permissions.")
    print()
    
    result = os.system(f"{sys.executable} authenticate.py")
    
    if result == 0 and os.path.exists('token.json'):
        print_success("Authentication successful!")
        return True
    else:
        print_error("Authentication failed")
        return False

def main():
    """Main setup wizard"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║          🎬 Video Automation Setup Wizard 🎬              ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    print("This wizard will guide you through setting up the video automation.")
    print("Make sure you have completed the prerequisites in SETUP.md\n")
    
    input("Press Enter to continue...")
    
    # Step 1: Check Python version
    if not check_python_version():
        print_error("\nSetup cannot continue. Please upgrade Python.")
        return
    
    # Step 2: Install dependencies
    install = get_input("\nInstall dependencies from requirements.txt? (yes/no)", default="yes")
    if install.lower() in ['yes', 'y']:
        if not install_dependencies():
            print_error("\nSetup cannot continue. Please fix dependency issues.")
            return
    
    # Step 3: Check credentials
    if not check_credentials_file():
        print_error("\nSetup cannot continue. Please add credentials.json")
        print_info("See SETUP.md Step 3.3 for instructions")
        return
    
    # Step 4: Create config
    if os.path.exists('config.py'):
        overwrite = get_input("\nconfig.py already exists. Overwrite? (yes/no)", default="no")
        if overwrite.lower() not in ['yes', 'y']:
            print_info("Skipping configuration creation")
        else:
            if not create_config():
                return
    else:
        if not create_config():
            return
    
    # Step 5: Authenticate
    auth = get_input("\nRun authentication now? (yes/no)", default="yes")
    if auth.lower() in ['yes', 'y']:
        if not run_authentication():
            print_warning("You can run authentication later with: python authenticate.py")
    
    # Success!
    print_header("Setup Complete!")
    print_success("Your video automation is ready to use!")
    print()
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print("  1. Run validation: python validate_setup.py")
    print("  2. Upload a test video to your Google Drive folder")
    print("  3. Start the automation: python main.py")
    print()
    print(f"{Colors.BOLD}Need help?{Colors.END}")
    print("  • Read TROUBLESHOOTING.md for common issues")
    print("  • Check FAQ.md for frequently asked questions")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled by user{Colors.END}")
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

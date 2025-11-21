"""
Validation script to check if the setup is complete and correct
"""
import os
import sys
import json

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_check(name, passed, message=""):
    """Print a check result"""
    if passed:
        print(f"{Colors.GREEN}✓{Colors.END} {name}")
        if message:
            print(f"  {Colors.BLUE}{message}{Colors.END}")
    else:
        print(f"{Colors.RED}✗{Colors.END} {name}")
        if message:
            print(f"  {Colors.YELLOW}{message}{Colors.END}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    if not exists:
        print_check(description, False, f"Missing: {filepath}")
    else:
        print_check(description, True, f"Found: {filepath}")
    return exists

def validate_credentials():
    """Validate credentials.json"""
    if not os.path.exists('credentials.json'):
        return False
    
    try:
        with open('credentials.json', 'r') as f:
            data = json.load(f)
            if 'installed' in data or 'web' in data:
                return True
    except:
        pass
    return False

def validate_config():
    """Validate config.py"""
    if not os.path.exists('config.py'):
        return False, []
    
    try:
        from config import Config
        issues = []
        
        # Check required fields
        if not hasattr(Config, 'DRIVE_FOLDER_ID') or 'YOUR_' in Config.DRIVE_FOLDER_ID:
            issues.append("DRIVE_FOLDER_ID not configured")
        
        if not hasattr(Config, 'GEMINI_API_KEY') or 'YOUR_' in Config.GEMINI_API_KEY:
            issues.append("GEMINI_API_KEY not configured")
        
        if not hasattr(Config, 'OPENAI_API_KEY') or 'YOUR_' in Config.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY not configured")
        
        if not hasattr(Config, 'SPREADSHEET_ID') or 'YOUR_' in Config.SPREADSHEET_ID:
            issues.append("SPREADSHEET_ID not configured")
        
        return len(issues) == 0, issues
    except Exception as e:
        return False, [f"Error loading config: {e}"]

def test_google_apis():
    """Test Google API connectivity"""
    results = {}
    
    # Test Drive API
    try:
        from services.drive_service import DriveService
        drive = DriveService()
        results['drive'] = True
    except Exception as e:
        results['drive'] = str(e)
    
    # Test YouTube API
    try:
        from services.youtube_service import YouTubeService
        youtube = YouTubeService()
        results['youtube'] = True
    except Exception as e:
        results['youtube'] = str(e)
    
    # Test Sheets API
    try:
        from services.sheets_service import SheetsService
        sheets = SheetsService()
        results['sheets'] = True
    except Exception as e:
        results['sheets'] = str(e)
    
    return results

def main():
    """Run all validation checks"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Video Automation Setup Validation{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    all_passed = True
    
    # Check files
    print(f"{Colors.BOLD}Checking Required Files...{Colors.END}\n")
    
    files_ok = True
    files_ok &= check_file_exists('credentials.json', 'OAuth Credentials')
    files_ok &= check_file_exists('config.py', 'Configuration File')
    files_ok &= check_file_exists('requirements.txt', 'Dependencies List')
    files_ok &= check_file_exists('main.py', 'Main Script')
    
    all_passed &= files_ok
    
    # Validate credentials
    print(f"\n{Colors.BOLD}Validating Credentials...{Colors.END}\n")
    creds_valid = validate_credentials()
    print_check("OAuth Credentials Valid", creds_valid, 
                "credentials.json is properly formatted" if creds_valid else "credentials.json is invalid or malformed")
    all_passed &= creds_valid
    
    # Validate config
    print(f"\n{Colors.BOLD}Validating Configuration...{Colors.END}\n")
    config_valid, config_issues = validate_config()
    
    if config_valid:
        print_check("Configuration Complete", True, "All required fields are configured")
    else:
        print_check("Configuration Complete", False, "Missing or invalid configuration:")
        for issue in config_issues:
            print(f"    {Colors.YELLOW}• {issue}{Colors.END}")
    
    all_passed &= config_valid
    
    # Check authentication
    print(f"\n{Colors.BOLD}Checking Authentication...{Colors.END}\n")
    token_exists = os.path.exists('token.json')
    print_check("OAuth Token", token_exists,
                "Authenticated" if token_exists else "Run: python authenticate.py")
    all_passed &= token_exists
    
    # Test API connectivity (only if authenticated)
    if token_exists and config_valid:
        print(f"\n{Colors.BOLD}Testing API Connectivity...{Colors.END}\n")
        
        api_results = test_google_apis()
        
        for api_name, result in api_results.items():
            if result is True:
                print_check(f"{api_name.title()} API", True, "Connection successful")
            else:
                print_check(f"{api_name.title()} API", False, f"Error: {result}")
                all_passed = False
    
    # Final summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed! Setup is complete.{Colors.END}")
        print(f"\n{Colors.BOLD}You're ready to run:{Colors.END}")
        print(f"  {Colors.BLUE}python main.py{Colors.END}\n")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please fix the issues above.{Colors.END}")
        print(f"\n{Colors.BOLD}Need help?{Colors.END}")
        print(f"  • Read SETUP.md for setup instructions")
        print(f"  • Check TROUBLESHOOTING.md for common issues\n")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validation cancelled{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Validation error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

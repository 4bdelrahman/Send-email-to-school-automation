"""
Setup Helper Script
Run this script once to authenticate with Gmail and generate token.json
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def setup_gmail_auth():
    """Initial Gmail authentication setup"""
    
    print("=" * 60)
    print("Gmail Auto-Sender - Initial Setup")
    print("=" * 60)
    print()
    
    # Check if OAuth.json exists
    if not os.path.exists('OAuth.json'):
        print("[ERROR] OAuth.json not found!")
        print()
        print("Please follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Enable Gmail API")
        print("3. Create OAuth 2.0 credentials (Desktop app)")
        print("4. Download OAuth.json to this directory")
        print()
        return False
    
    print("[OK] Found OAuth.json")
    print()
    
    # Check if token already exists
    if os.path.exists('token.json'):
        print("[WARNING] token.json already exists!")
        response = input("Do you want to re-authenticate? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
        print()
    
    # Run OAuth flow
    print("Starting OAuth authentication...")
    print("A browser window will open. Please:")
    print("1. Select your Google account (ammell.ommarr37@gmail.com)")
    print("2. Grant permissions to access Gmail")
    print("3. Close the browser when done")
    print()
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file('OAuth.json', SCOPES)
        # prompt='consent' ensures a refresh_token is returned every time
        # access_type='offline' is required for refresh_tokens
        creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
        
        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        print()
        print("=" * 60)
        print("[SUCCESS] Authentication complete!")
        print("=" * 60)
        print()
        print("token.json has been created.")
        print()
        print("Next steps:")
        print("1. Test locally: python execution/gmail_auto_sender.py")
        print("2. Add GitHub Secrets:")
        print("   - GMAIL_CREDENTIALS (content of OAuth.json)")
        print("   - GMAIL_TOKEN (content of token.json)")
        print("   - MONITORING_EMAIL (ammell.ommarr37@gmail.com)")
        print("   - TARGET_EMAIL (DP@eis-zayed.com)")
        print("3. Enable GitHub Actions")
        print()
        
        return True
    
    except Exception as e:
        print()
        print("[ERROR] Authentication failed!")
        print(f"Error: {e}")
        print()
        return False


if __name__ == '__main__':
    setup_gmail_auth()

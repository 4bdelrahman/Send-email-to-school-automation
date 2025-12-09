"""
Gmail Auto-Sender Script
Monitors Gmail inbox for !send command and sends pre-formatted email to DP@eis-zayed.com
"""

import os
import base64
from datetime import datetime
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Configuration
MONITORING_EMAIL = os.getenv('MONITORING_EMAIL')
TARGET_EMAIL = os.getenv('TARGET_EMAIL', 'DP@eis-zayed.com')
LOG_FILE = '.tmp/email_log.txt'


def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('OAuth.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)


def create_message(to, subject, body):
    """Create email message"""
    message = MIMEText(body, 'plain', 'utf-8')
    message['to'] = to
    message['subject'] = subject
    
    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def send_dismissal_email(service, date_str=None):
    """Send the pre-formatted dismissal email"""
    
    # Use current date if not provided
    if not date_str:
        date_str = datetime.now().strftime('%d/%m/%Y')
    
    subject = "طلب انصراف مبكر"
    body = f"""صباح الخير مستر / محمد بديع

ارجو السماح للطالب / عبدالرحمن احمد شحاته بالانصراف اليوم {date_str} بعد البريك الاول

شكرا لحضرتك
والدة الطالب / امل كمال
بطاقة / 28004300100466"""
    
    try:
        message = create_message(TARGET_EMAIL, subject, body)
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        
        log_message = f"[{datetime.now()}] Email sent successfully to {TARGET_EMAIL}. Message ID: {sent_message['id']}\n"
        print(log_message)
        
        # Log to file
        os.makedirs('.tmp', exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message)
        
        return True
    
    except HttpError as error:
        error_msg = f"[{datetime.now()}] Error sending email: {error}\n"
        print(error_msg)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(error_msg)
        return False


def check_for_send_command(service):
    """Check inbox for unread emails with !send command"""
    
    try:
        # Search for unread messages containing !send
        query = 'is:unread (!send OR "!send")'
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print(f"[{datetime.now()}] No !send commands found.")
            return []
        
        print(f"[{datetime.now()}] Found {len(messages)} message(s) with !send command.")
        return messages
    
    except HttpError as error:
        print(f"[{datetime.now()}] Error checking messages: {error}")
        return []


def mark_as_read(service, message_id):
    """Mark message as read"""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"[{datetime.now()}] Marked message {message_id} as read.")
    except HttpError as error:
        print(f"[{datetime.now()}] Error marking message as read: {error}")


def process_messages(service, messages):
    """Process all messages with !send command"""
    
    for msg in messages:
        message_id = msg['id']
        
        # Get message details
        try:
            message = service.users().messages().get(userId='me', id=message_id).execute()
            
            # Extract date if present in the message (optional enhancement)
            # For now, use current date
            
            # Send the dismissal email
            success = send_dismissal_email(service)
            
            if success:
                # Mark the trigger email as read
                mark_as_read(service, message_id)
                
                # Optional: Add a label
                # apply_label(service, message_id, 'Processed')
        
        except HttpError as error:
            print(f"[{datetime.now()}] Error processing message {message_id}: {error}")


def main():
    """Main execution function"""
    print(f"[{datetime.now()}] Starting Gmail Auto-Sender...")
    
    # Get Gmail service
    service = get_gmail_service()
    
    # Check for !send commands
    messages = check_for_send_command(service)
    
    # Process messages
    if messages:
        process_messages(service, messages)
        print(f"[{datetime.now()}] Processing complete. {len(messages)} email(s) processed.")
    else:
        print(f"[{datetime.now()}] No messages to process.")


if __name__ == '__main__':
    main()

"""
Gmail Auto-Sender Script
Monitors Gmail inbox for !send command and sends pre-formatted email to DP@eis-zayed.com
FIXED: Only processes ONE email at a time, only recent emails (last 24 hours)
"""

import os
import base64
from datetime import datetime, timedelta
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
MONITORING_EMAIL = os.getenv('MONITORING_EMAIL', 'ammell.ommarr37@gmail.com')
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


def get_email_body(service, message_id):
    """Extract the body text from an email"""
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        
        # Try to get body from payload
        payload = message.get('payload', {})
        
        # Check for simple body
        if 'body' in payload and payload['body'].get('data'):
            body_data = payload['body']['data']
            return base64.urlsafe_b64decode(body_data).decode('utf-8')
        
        # Check for multipart message
        parts = payload.get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                if 'body' in part and part['body'].get('data'):
                    body_data = part['body']['data']
                    return base64.urlsafe_b64decode(body_data).decode('utf-8')
        
        # Fallback: return snippet
        return message.get('snippet', '')
    
    except Exception as e:
        print(f"Error getting email body: {e}")
        return ''


def check_for_send_command(service):
    """Check inbox for unread emails with !send command from last 24 hours"""
    
    try:
        # Only check emails from the last 24 hours
        yesterday = (datetime.now() - timedelta(hours=24)).strftime('%Y/%m/%d')
        
        # Search for unread messages from last 24 hours
        query = f'is:unread after:{yesterday}'
        results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print(f"[{datetime.now()}] No unread emails from last 24 hours.")
            return None
        
        print(f"[{datetime.now()}] Found {len(messages)} recent unread email(s). Checking for !send command...")
        
        # Check each message for !send in the body
        for msg in messages:
            message_id = msg['id']
            body = get_email_body(service, message_id)
            
            # Check if !send is in the body (case insensitive)
            if '!send' in body.lower():
                print(f"[{datetime.now()}] Found !send command in message {message_id}")
                return msg  # Return ONLY the first matching message
        
        print(f"[{datetime.now()}] No emails with !send command found.")
        return None
    
    except HttpError as error:
        print(f"[{datetime.now()}] Error checking messages: {error}")
        return None


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


def main():
    """Main execution function"""
    print(f"[{datetime.now()}] Starting Gmail Auto-Sender...")
    print(f"[{datetime.now()}] Monitoring: {MONITORING_EMAIL}")
    print(f"[{datetime.now()}] Target: {TARGET_EMAIL}")
    print()
    
    # Get Gmail service
    service = get_gmail_service()
    
    # Check for !send command (returns only ONE message)
    message = check_for_send_command(service)
    
    # Process the message if found
    if message:
        message_id = message['id']
        
        print(f"[{datetime.now()}] Processing message {message_id}...")
        
        # Send the dismissal email (ONE email only)
        success = send_dismissal_email(service)
        
        if success:
            # Mark the trigger email as read
            mark_as_read(service, message_id)
            print(f"[{datetime.now()}] SUCCESS: Sent 1 dismissal email to {TARGET_EMAIL}")
        else:
            print(f"[{datetime.now()}] FAILED: Could not send email")
    else:
        print(f"[{datetime.now()}] No !send command found. Nothing to process.")


if __name__ == '__main__':
    main()

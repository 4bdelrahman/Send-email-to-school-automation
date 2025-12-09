# Gmail Auto-Send Directive

## Goal
Monitor a specific Gmail inbox for emails containing the command `!send`. When detected, automatically send a pre-formatted Arabic email to DP@eis-zayed.com requesting early dismissal for the student.

## Inputs
- **Monitoring Email**: ammell.ommarr37@gmail.com (receives the `!send` command)
- **Command Trigger**: `!send` in the email body or subject
- **Target Email**: DP@eis-zayed.com
- **Email Template**: Pre-formatted Arabic message requesting student dismissal
- **Credentials**: OAuth.json file containing Google OAuth 2.0 credentials

## Process Flow

1. **Authentication**
   - Use Gmail API with OAuth 2.0
   - Read credentials from `OAuth.json` file
   - Token stored in `token.json` (auto-refreshed)

2. **Email Monitoring**
   - Check for new unread emails in monitoring inbox
   - Search for emails containing `!send` command
   - Can be triggered by GitHub Actions on a schedule (e.g., every 5 minutes)

3. **Command Detection**
   - Parse email body and subject for `!send` trigger
   - Validate that the command is present
   - Extract any additional context if needed (date, time, etc.)

4. **Email Sending**
   - Compose email with Arabic template
   - Send from the authenticated Gmail account
   - Target: DP@eis-zayed.com
   - Subject: طلب انصراف مبكر (Early Dismissal Request)
   - Body: Pre-formatted Arabic message

5. **Post-Processing**
   - Mark the trigger email as read
   - Optionally apply a label (e.g., "Processed")
   - Log the action to `.tmp/email_log.txt`

## Email Template

**Subject**: طلب انصراف مبكر

**Body**:
```
صباح الخير مستر / محمد بديع

ارجو السماح للطالب / عبدالرحمن احمد شحاته بالانصراف اليوم {DATE} بعد البريك الاول

شكرا لحضرتك
والدة الطالب / امل كمال
بطاقة / 28004300100466
```

## Tools/Scripts

### Primary Script
- `execution/gmail_auto_sender.py` - Main script that monitors and sends emails

### Helper Scripts (if needed)
- `execution/gmail_auth.py` - Handle Gmail OAuth authentication
- `execution/email_template.py` - Manage email templates

## Outputs

### Deliverables
- Email sent to DP@eis-zayed.com
- Confirmation logged in monitoring system

### Intermediates
- `.tmp/email_log.txt` - Log of all processed emails
- `.tmp/last_check.txt` - Timestamp of last check (for incremental monitoring)

## Edge Cases

1. **Multiple !send commands**: Process all unread emails with the command
2. **Invalid date format**: Use current date if no date specified
3. **API rate limits**: Gmail API has quotas (check and handle gracefully)
4. **Authentication failure**: Log error and notify (don't crash)
5. **Network issues**: Retry with exponential backoff
6. **Duplicate processing**: Track processed message IDs to avoid duplicates

## GitHub Actions Integration

- Schedule: Every 10 minutes, 24/7 (anytime, any day)
- Use GitHub Secrets for credentials
- Workflow file: `.github/workflows/gmail_monitor.yml`

## Environment Variables Required

```
GMAIL_CLIENT_ID=<from OAuth.json>
GMAIL_CLIENT_SECRET=<from OAuth.json>
GMAIL_REFRESH_TOKEN=<generated during OAuth flow>
MONITORING_EMAIL=ammell.ommarr37@gmail.com
TARGET_EMAIL=DP@eis-zayed.com
```

## Setup Steps

1. Enable Gmail API in Google Cloud Console
2. Create OAuth 2.0 credentials (Desktop app)
3. Download credential file as `OAuth.json`
4. Run initial authentication to get refresh token
5. Store credentials in `.env` locally and GitHub Secrets for Actions
6. Test script locally first
7. Deploy to GitHub Actions

## Success Criteria

- Email is sent within 5 minutes of receiving `!send` command
- No duplicate emails sent
- Proper error handling and logging
- Works reliably in GitHub Actions environment

## Notes

- Gmail API quota: 1 billion quota units per day (sending = 100 units)
- OAuth token auto-refreshes, no manual intervention needed
- Keep OAuth.json and token.json files secure (gitignored)
- Upload OAuth.json content to GitHub Secrets as GMAIL_CREDENTIALS
- Date in email template is automatically set to current date
- Monitoring email: ammell.ommarr37@gmail.com
- Test thoroughly before deploying to production

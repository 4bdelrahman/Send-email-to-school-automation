# Gmail Auto-Sender Automation

Automated Gmail monitoring system that sends pre-formatted emails when triggered by a `!send` command. Built using the 3-layer architecture (Directive → Orchestration → Execution).

## 🎯 Purpose

This system monitors a Gmail inbox for emails containing the `!send` command. When detected, it automatically sends a pre-formatted Arabic email to DP@eis-zayed.com requesting early dismissal for the student.

## 🏗️ Architecture

Following the 3-layer architecture defined in `Agent.md`:

- **Layer 1 (Directive)**: `directives/gmail_auto_send.md` - Defines what to do
- **Layer 2 (Orchestration)**: AI agent reads directive and calls execution scripts
- **Layer 3 (Execution)**: `execution/gmail_auto_sender.py` - Deterministic Python script

## 📁 Project Structure

```
Auto email sender/
├── .github/
│   └── workflows/
│       └── gmail_monitor.yml      # GitHub Actions workflow
├── .tmp/                          # Temporary files (gitignored)
│   └── email_log.txt             # Email processing logs
├── directives/
│   └── gmail_auto_send.md        # SOP for Gmail automation
├── execution/
│   └── gmail_auto_sender.py      # Main execution script
├── .env                          # Environment variables (gitignored)
├── .env.example                  # Template for .env
├── .gitignore                    # Git ignore rules
├── Agent.md                      # Architecture documentation
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Setup Instructions


### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your details:
   ```
   MONITORING_EMAIL=your_email@gmail.com
   TARGET_EMAIL=DP@eis-zayed.com
   ```

### 4. Initial Authentication

Run the script locally once to authenticate:

```bash
python execution/gmail_auto_sender.py
```

This will:
- Open a browser for Google OAuth (using OAuth.json)
- Generate `token.json` file (auto-refreshes in future)
- Check for `!send` commands and process them

### 5. Deploy to GitHub Actions

1. **Push code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Gmail auto-sender"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Add GitHub Secrets**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `GMAIL_CREDENTIALS`: Content of `OAuth.json`
     - `GMAIL_TOKEN`: Content of `token.json`
     - `MONITORING_EMAIL`: Your monitoring email
     - `TARGET_EMAIL`: `DP@eis-zayed.com`

3. **Enable GitHub Actions**:
   - Go to Actions tab and enable workflows
   - The workflow runs every 10 minutes during school hours (7 AM - 3 PM Egypt time)

## 📧 How It Works

1. **Trigger**: Send an email to your monitoring email with `!send` in the body or subject
2. **Detection**: GitHub Actions runs every 10 minutes and checks for unread emails with `!send`
3. **Processing**: Script sends the pre-formatted email to DP@eis-zayed.com
4. **Cleanup**: Marks the trigger email as read
5. **Logging**: Logs all actions to `.tmp/email_log.txt`

## 📝 Email Template

**To**: DP@eis-zayed.com  
**Subject**: طلب انصراف مبكر

**Body**:
```
صباح الخير مستر / محمد بديع

ارجو السماح للطالب / عبدالرحمن احمد شحاته بالانصراف اليوم [DATE] بعد البريك الاول

شكرا لحضرتك
والدة الطالب / امل كمال
بطاقة / 28004300100466
```

## 🔧 Manual Testing

Test the workflow manually:

```bash
# Run locally
python execution/gmail_auto_sender.py

# Or trigger GitHub Actions manually
# Go to Actions tab → Gmail Auto-Sender Monitor → Run workflow
```

## 📊 Monitoring

- **Logs**: Check `.tmp/email_log.txt` for processing history
- **GitHub Actions**: View workflow runs in the Actions tab
- **Artifacts**: Download email logs from completed workflow runs

## ⚙️ Configuration

### Schedule (in `.github/workflows/gmail_monitor.yml`)

Default: Every 10 minutes, 24/7 (any time, any day)

To change frequency, edit the cron expression:
```yaml
schedule:
  - cron: '*/10 * * * *'
```

### Email Template

To modify the email content, edit the `send_dismissal_email()` function in `execution/gmail_auto_sender.py`.

## 🛡️ Security

- Never commit `OAuth.json`, `token.json`, or `.env` to Git
- Use GitHub Secrets for sensitive data
- Gmail API uses OAuth 2.0 for secure authentication
- Tokens auto-refresh, no password storage needed

## 🐛 Troubleshooting

### Authentication Issues
- Delete `token.json` and re-authenticate
- Ensure `OAuth.json` is valid
- Check OAuth consent screen configuration

### No Emails Sent
- Verify `!send` command is in email body/subject
- Check email is unread
- Review logs in `.tmp/email_log.txt`
- Ensure GitHub Secrets are configured correctly

### Rate Limits
- Gmail API quota: 1 billion units/day
- Sending email = 100 units
- Current schedule is well within limits

## 📚 Resources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

## 🤝 Contributing

This project follows the 3-layer architecture. When making changes:

1. Update the directive in `directives/gmail_auto_send.md`
2. Modify execution scripts in `execution/`
3. Test locally before deploying
4. Update this README if needed

## 📄 License

MIT License - feel free to modify and use as needed.

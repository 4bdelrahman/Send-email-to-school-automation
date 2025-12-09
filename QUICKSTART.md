# Quick Start Guide

## 🚀 Get Started in 5 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Gmail API**
4. Create **OAuth 2.0 Client ID** (Desktop app type)
5. Download `OAuth.json` and place in project root

### Step 3: Run Initial Setup
```bash
python setup.py
```

This will:
- Open a browser for Google OAuth
- Generate `token.json` file
- Verify authentication works

### Step 4: Test Locally

1. Send yourself an email with `!send` in the body
2. Run the script:
   ```bash
   python execution/gmail_auto_sender.py
   ```
3. Check if email was sent to DP@eis-zayed.com

### Step 5: Deploy to GitHub Actions

1. **Create GitHub repository** and push code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Add GitHub Secrets** (Settings → Secrets → Actions):
   - `GMAIL_CREDENTIALS`: Paste entire content of `OAuth.json`
   - `GMAIL_TOKEN`: Paste entire content of `token.json`
   - `MONITORING_EMAIL`: Your Gmail address
   - `TARGET_EMAIL`: `DP@eis-zayed.com`

3. **Enable GitHub Actions**:
   - Go to Actions tab
   - Enable workflows
   - Done! It will run every 10 minutes during school hours

## 📧 How to Use

1. Send an email to your monitoring email
2. Include `!send` anywhere in the subject or body
3. Within 10 minutes, the system will:
   - Detect the command
   - Send the dismissal email to DP@eis-zayed.com
   - Mark your email as read

## 🔍 Verify It's Working

- **Check logs**: `.tmp/email_log.txt`
- **GitHub Actions**: View workflow runs in Actions tab
- **Email sent**: Check DP@eis-zayed.com inbox

## ⚡ Manual Trigger

You can manually trigger the workflow:
- Go to GitHub → Actions → Gmail Auto-Sender Monitor → Run workflow

## 🆘 Need Help?

See `README.md` for detailed documentation and troubleshooting.

## 📝 Important Files

- `OAuth.json` - Gmail API credentials (DO NOT COMMIT)
- `token.json` - OAuth token (DO NOT COMMIT)
- `.env` - Environment variables (DO NOT COMMIT)
- All sensitive files are in `.gitignore`

## ✅ Checklist

- [ ] Installed dependencies
- [ ] Created Google Cloud project
- [ ] Downloaded OAuth.json
- [ ] Ran setup.py successfully
- [ ] Tested locally
- [ ] Created GitHub repository
- [ ] Added GitHub Secrets
- [ ] Enabled GitHub Actions
- [ ] Sent test email with !send
- [ ] Verified email received at DP@eis-zayed.com

---

**You're all set! 🎉**

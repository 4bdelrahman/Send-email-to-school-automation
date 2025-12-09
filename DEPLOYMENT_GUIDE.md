# Deployment Guide

This guide will help you deploy the Gmail Auto-Sender to your GitHub repository and configure it to run automatically.

## 📋 Prerequisites Checklist

Before deploying, make sure you have:

- [ ] OAuth.json file (downloaded from Google Cloud Console)
- [ ] Completed initial setup locally (`python setup.py`)
- [ ] token.json file (generated after authentication)
- [ ] Tested locally and verified it works (`python execution/gmail_auto_sender.py`)

## 🚀 Step 1: Push Code to GitHub

Your repository is already created at: https://github.com/4bdelrahman/Send-email-to-school-automation.git

```bash
# Navigate to your project directory
cd "c:/Users/hp/OneDrive/Desktop/Coding/Antigravity/Auto email sender"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: Gmail auto-sender with OAuth.json"

# Add your remote repository
git remote add origin https://github.com/4bdelrahman/Send-email-to-school-automation.git

# Push to GitHub
git push -u origin main
```

**Note**: If you get an error about the branch name, try:
```bash
git branch -M main
git push -u origin main
```

## 🔐 Step 2: Configure GitHub Secrets

After pushing the code, configure the secrets:

### 2.1 Go to Repository Settings
1. Visit https://github.com/4bdelrahman/Send-email-to-school-automation/settings/secrets/actions
2. Click "New repository secret"

### 2.2 Add Required Secrets

Add these 4 secrets:

#### Secret 1: GMAIL_CREDENTIALS
- **Name**: `GMAIL_CREDENTIALS`
- **Value**: Open `OAuth.json` in a text editor, copy **ENTIRE content**, paste as value

#### Secret 2: GMAIL_TOKEN
- **Name**: `GMAIL_TOKEN`
- **Value**: Open `token.json` in a text editor, copy **ENTIRE content**, paste as value

#### Secret 3: MONITORING_EMAIL
- **Name**: `MONITORING_EMAIL`
- **Value**: `ammell.ommarr37@gmail.com`

#### Secret 4: TARGET_EMAIL
- **Name**: `TARGET_EMAIL`
- **Value**: `DP@eis-zayed.com`

## ✅ Step 3: Enable GitHub Actions

1. Go to https://github.com/4bdelrahman/Send-email-to-school-automation/actions
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. You should see "Gmail Auto-Sender Monitor" workflow listed

## 🧪 Step 4: Test the Workflow

### Manual Test (Recommended First)
1. Go to https://github.com/4bdelrahman/Send-email-to-school-automation/actions
2. Click on "Gmail Auto-Sender Monitor"
3. Click "Run workflow" dropdown
4. Click green "Run workflow" button
5. Wait for it to complete (should take ~1 minute)
6. Check for green checkmark ✅

### Live Test
1. Send an email to **ammell.ommarr37@gmail.com**
2. Include `!send` in the subject or body
3. Mark the email as unread (important!)
4. Wait up to 10 minutes
5. Check if email was sent to DP@eis-zayed.com

## 📊 Monitoring Your Workflow

### View Workflow Runs
- URL: https://github.com/4bdelrahman/Send-email-to-school-automation/actions

### Check Logs
1. Click on any workflow run
2. Click on "monitor-and-send" job
3. Expand steps to see detailed logs
4. Look for "Run Gmail Auto-Sender" step

### Download Logs
1. Scroll to "Artifacts" section at bottom of workflow run
2. Download "email-logs" if available

## ⏰ Schedule Information

The workflow runs:
- **Every 10 minutes**
- **24/7** (anytime, any day)
- Checks for new emails with `!send` command

To change the schedule, edit `.github/workflows/gmail_monitor.yml`:
```yaml
schedule:
  - cron: '*/10 * * * *'  # Every 10 minutes
```

## 🎯 How to Use

Once deployed:

1. **Send trigger email** to ammell.ommarr37@gmail.com with `!send` in body/subject
2. **Wait** (up to 10 minutes for next scheduled run)
3. **Automated email sent** to DP@eis-zayed.com with current date
4. **Trigger email marked as read** automatically

## 🔧 Troubleshooting

### Workflow Not Running
- Check that secrets are configured correctly
- Verify workflow is enabled in Actions tab
- Check if it's within the scheduled time (7 AM - 3 PM Egypt time, Mon-Fri)

### Authentication Errors
- Verify GMAIL_CREDENTIALS contains valid JSON
- Verify GMAIL_TOKEN contains valid JSON
- Try re-running `setup.py` locally to regenerate token.json

### Email Not Sent
- Ensure trigger email contains `!send`
- Verify trigger email is unread
- Check workflow logs for errors
- Verify monitoring email is ammell.ommarr37@gmail.com

### Secrets Not Working
- Secret names must match EXACTLY (case-sensitive)
- No extra spaces in secret values
- JSON secrets must be complete and valid

## 📝 Quick Reference

| Item | Value |
|------|-------|
| Repository | https://github.com/4bdelrahman/Send-email-to-school-automation.git |
| Monitoring Email | ammell.ommarr37@gmail.com |
| Target Email | DP@eis-zayed.com |
| Trigger Command | `!send` |
| Schedule | Every 10 min, 24/7 |
| Workflow File | `.github/workflows/gmail_monitor.yml` |

## ✨ Success Indicators

Your deployment is successful when:

- ✅ Code pushed to GitHub without errors
- ✅ All 4 secrets configured
- ✅ Workflow appears in Actions tab
- ✅ Manual test run completes successfully
- ✅ Test email with `!send` triggers automation
- ✅ Email delivered to DP@eis-zayed.com
- ✅ Trigger email marked as read

## 🎉 Next Steps

After successful deployment:

1. **Monitor for a day** to ensure reliability
2. **Check logs regularly** for any issues
3. **Update directive** if you discover edge cases
4. **Share your success!**

## 📞 Support

If you encounter issues:

1. Check the logs in GitHub Actions
2. Review the troubleshooting section above
3. Verify all secrets are correct
4. Test locally to isolate the issue

---

**You're ready to deploy! 🚀**

Start with Step 1 and work through each step carefully. Good luck!

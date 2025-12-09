# Setup Checklist

Use this checklist to track your progress setting up the Gmail Auto-Sender.

## Phase 1: Local Setup

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Gmail account ready
- [ ] Google Cloud account (free tier is fine)

### Install Dependencies
```bash
pip install -r requirements.txt
```
- [ ] Dependencies installed successfully
- [ ] No errors during installation

### Google Cloud Setup
1. [ ] Go to https://console.cloud.google.com/
2. [ ] Create new project (or select existing)
3. [ ] Enable Gmail API
   - [ ] Search for "Gmail API" in search bar
   - [ ] Click "Enable"
4. [ ] Create OAuth 2.0 credentials
   - [ ] Go to Credentials → Create Credentials
   - [ ] Select "OAuth client ID"
   - [ ] Application type: "Desktop app"
   - [ ] Name it (e.g., "Gmail Auto-Sender")
5. [ ] Download credentials
   - [ ] Click download icon
   - [ ] Save as `credentials.json` in project root

### Initial Authentication
```bash
python setup.py
```
- [ ] Browser opened for OAuth
- [ ] Selected Google account
- [ ] Granted permissions
- [ ] `token.json` created successfully
- [ ] No errors in console

### Local Testing
1. [ ] Send test email to yourself with `!send` in body
2. [ ] Run: `python execution/gmail_auto_sender.py`
3. [ ] Check console output for success message
4. [ ] Verify email sent to DP@eis-zayed.com
5. [ ] Check `.tmp/email_log.txt` for log entry
6. [ ] Verify trigger email marked as read

**Local Setup Complete!** ✅

---

## Phase 2: GitHub Deployment

### Create Repository
```bash
git init
git add .
git commit -m "Initial commit: Gmail auto-sender"
```
- [ ] Git repository initialized
- [ ] Files committed
- [ ] No sensitive files in commit (check with `git status`)

### Push to GitHub
1. [ ] Create repository on GitHub
2. [ ] Copy repository URL
3. [ ] Run commands:
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
4. [ ] Code pushed successfully
5. [ ] Verify files on GitHub

### Configure GitHub Secrets
Go to: Repository → Settings → Secrets and variables → Actions → New repository secret

1. [ ] **GMAIL_CREDENTIALS**
   - Open `credentials.json` in text editor
   - Copy entire content
   - Paste as secret value

2. [ ] **GMAIL_TOKEN**
   - Open `token.json` in text editor
   - Copy entire content
   - Paste as secret value

3. [ ] **MONITORING_EMAIL**
   - Enter your Gmail address
   - Example: `yourname@gmail.com`

4. [ ] **TARGET_EMAIL**
   - Enter: `DP@eis-zayed.com`

### Enable GitHub Actions
1. [ ] Go to Actions tab
2. [ ] Enable workflows (if prompted)
3. [ ] Verify "Gmail Auto-Sender Monitor" appears

### Test GitHub Actions
1. [ ] Click on workflow name
2. [ ] Click "Run workflow" dropdown
3. [ ] Click "Run workflow" button
4. [ ] Wait for workflow to complete
5. [ ] Check for green checkmark ✅
6. [ ] Review logs for any errors
7. [ ] Download artifacts (if available)

**GitHub Deployment Complete!** ✅

---

## Phase 3: Production Testing

### End-to-End Test
1. [ ] Send email with `!send` to monitoring email
2. [ ] Wait up to 10 minutes
3. [ ] Check GitHub Actions for new run
4. [ ] Verify workflow completed successfully
5. [ ] Check DP@eis-zayed.com inbox for email
6. [ ] Verify trigger email marked as read

### Schedule Verification
- [ ] Workflow runs during school hours (7 AM - 3 PM Egypt time)
- [ ] Workflow does NOT run outside school hours
- [ ] Workflow runs Monday - Friday only

### Error Handling Test
1. [ ] Test with invalid email format
2. [ ] Test with multiple `!send` commands
3. [ ] Test during off-hours
4. [ ] Verify errors logged properly

**Production Testing Complete!** ✅

---

## Phase 4: Monitoring & Maintenance

### Regular Checks
- [ ] Check GitHub Actions weekly for failures
- [ ] Review `.tmp/email_log.txt` periodically
- [ ] Monitor Gmail API quota usage
- [ ] Verify emails still being sent correctly

### Documentation
- [ ] Read `README.md` fully
- [ ] Understand `WORKFLOW.md` diagrams
- [ ] Review `directives/gmail_auto_send.md`
- [ ] Bookmark troubleshooting section

### Backup
- [ ] Save `credentials.json` securely (NOT in Git)
- [ ] Save `token.json` securely (NOT in Git)
- [ ] Document any custom changes made

---

## Troubleshooting Checklist

If something goes wrong, check these:

### Authentication Issues
- [ ] `credentials.json` exists and is valid
- [ ] `token.json` exists and is valid
- [ ] OAuth consent screen configured correctly
- [ ] Gmail API enabled in Google Cloud

### Email Not Sending
- [ ] Email contains `!send` (case-insensitive)
- [ ] Email is unread
- [ ] GitHub Actions running on schedule
- [ ] Secrets configured correctly
- [ ] No API quota exceeded

### GitHub Actions Failing
- [ ] All 4 secrets configured
- [ ] Secrets contain valid JSON (for credentials/token)
- [ ] Workflow file syntax correct
- [ ] Dependencies installing successfully

### Network/API Issues
- [ ] Internet connection stable
- [ ] Gmail API not down (check status page)
- [ ] GitHub Actions not experiencing outages
- [ ] No rate limiting from Gmail

---

## Success Metrics

Your system is fully operational when:

- ✅ Emails sent within 10 minutes of `!send` command
- ✅ No duplicate emails sent
- ✅ Trigger emails marked as read
- ✅ Logs show successful operations
- ✅ GitHub Actions runs without errors
- ✅ Works during school hours only
- ✅ No manual intervention needed

---

## Next Steps After Setup

Once everything is working:

1. [ ] Test for a full week to ensure reliability
2. [ ] Document any edge cases in directive
3. [ ] Consider adding email notifications for failures
4. [ ] Optimize schedule if needed
5. [ ] Share success with others! 🎉

---

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Initial setup | `python setup.py` |
| Test locally | `python execution/gmail_auto_sender.py` |
| View logs | `cat .tmp/email_log.txt` |
| Push to GitHub | `git push origin main` |

---

**Current Status**: ⬜ Not Started / 🟡 In Progress / ✅ Complete

Mark your overall progress:
- [ ] Phase 1: Local Setup
- [ ] Phase 2: GitHub Deployment  
- [ ] Phase 3: Production Testing
- [ ] Phase 4: Monitoring & Maintenance

**Good luck! 🚀**

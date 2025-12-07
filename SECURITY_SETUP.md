# Security Setup - Quick Reference

## 🚀 Quick Start (5 Minutes)

### For Local Development

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   ADMIN_DEFAULT_PASSWORD=YourSecurePassword123!
   ```

3. **Run with environment variables:**
   
   **Windows PowerShell:**
   ```powershell
   Get-Content .env | ForEach-Object {
       if ($_ -match '^([^=]+)=(.*)$') {
           [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
       }
   }
   streamlit run rcm_fmeca_app.py
   ```
   
   **Linux/Mac:**
   ```bash
   export $(cat .env | xargs)
   streamlit run rcm_fmeca_app.py
   ```

### For Streamlit Cloud

1. **Push to GitHub** (secrets are excluded automatically)
2. **Deploy on Streamlit Cloud:** https://share.streamlit.io
3. **Add secrets** in App Settings → Secrets:
   ```toml
   ADMIN_DEFAULT_PASSWORD = "YourSecurePassword123!"
   ```

### For Other Cloud Platforms

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Heroku
- AWS (EC2, Elastic Beanstalk)
- Google Cloud (Cloud Run, App Engine)
- Azure App Service
- Docker deployment

## 📋 Security Checklist

### Before First Commit
- [ ] Verify `.env` is in `.gitignore`
- [ ] Verify `.users.json` is in `.gitignore`
- [ ] Verify `.registration` is in `.gitignore`
- [ ] Run `git status` to check no sensitive files are staged
- [ ] Ensure only `.env.example` is committed (template only)

### Before Deployment
- [ ] Set `ADMIN_DEFAULT_PASSWORD` environment variable
- [ ] Use strong password (12+ characters, mixed case, numbers, symbols)
- [ ] Test login with new password
- [ ] Document password in secure password manager
- [ ] Remove any test `.users.json` files

### After Deployment
- [ ] Login as admin with custom password
- [ ] Create user accounts for team members
- [ ] Assign appropriate user types (User, Super User, Administrator)
- [ ] Test that regular users cannot access Administration
- [ ] Change admin password regularly (every 90 days recommended)

## 🔐 What's Protected

### Never Committed to Git (in .gitignore)
✅ `.env` - Your environment variables with passwords  
✅ `.users.json` - User accounts with hashed passwords  
✅ `.registration` - Organization registration details  
✅ `.autosave.json` - Project analysis data  

### Safe to Commit
✅ `.env.example` - Template showing required variables (NO SECRETS)  
✅ `.gitignore` - Git exclusion rules  
✅ `rcm_fmeca_app.py` - Application code  
✅ `*.md` - Documentation files  
✅ All other source code files  

## 🎯 Environment Variables Reference

| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `ADMIN_DEFAULT_PASSWORD` | Default admin password | `odyssey` | Recommended |

## 🆘 Common Issues

### Issue: Using default password in production
**Solution:** Set `ADMIN_DEFAULT_PASSWORD` environment variable

### Issue: Can't login after setting environment variable
**Solution:** 
1. Delete `.users.json` file
2. Restart application
3. New admin account will be created with new password

### Issue: Accidentally committed sensitive files
**Solution:**
```bash
# Remove from Git but keep local file
git rm --cached .env
git rm --cached .users.json
git rm --cached .registration

# Commit the removal
git commit -m "Remove sensitive files"
git push
```

### Issue: Sensitive files in Git history
**Solution:** See "If Files Are Already in GitHub History" section in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📚 More Information

- **Complete deployment instructions:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **User authentication details:** [REGISTRATION_INFO.md](REGISTRATION_INFO.md)
- **Quick start guide:** [QUICK_START.md](QUICK_START.md)
- **Full documentation:** [README.md](README.md)

## 🔄 Password Rotation

**Recommended: Every 90 days**

1. Set new `ADMIN_DEFAULT_PASSWORD` in environment
2. Delete `.users.json` from deployment
3. Restart application
4. Test login with new password
5. Notify all users of the change
6. Users re-register or admin recreates accounts

---

**Last Updated:** December 7, 2025  
**Version:** 1.0.2+

# Deployment Guide - Environment Variables

## Overview

This guide explains how to configure sensitive settings using environment variables for local development, GitHub, and cloud deployment.

## Security Architecture

### Protected Files (Never Commit)
- `.env` - Environment variables (local development)
- `.users.json` - User accounts and passwords
- `.registration` - Organization details
- `.autosave.json` - Project data

### Safe to Commit
- `.env.example` - Template showing required variables (no actual secrets)
- `rcm_fmeca_app.py` - Application code
- Documentation files

## Environment Variables

### ADMIN_DEFAULT_PASSWORD

**Purpose**: Sets the default password for the `admin` account created on first run.

**Default**: `odyssey` (if not set)

**Security**: Change this in production environments!

## Local Development Setup

### Option 1: Using .env File (Recommended)

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```bash
   # .env file
   ADMIN_DEFAULT_PASSWORD=MySecurePassword123!
   ```

3. **Load environment variables before running:**
   
   **Windows (PowerShell):**
   ```powershell
   # Load from .env file
   Get-Content .env | ForEach-Object {
       if ($_ -match '^([^=]+)=(.*)$') {
           [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
       }
   }
   
   # Run application
   streamlit run rcm_fmeca_app.py
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   # Set variables manually
   set ADMIN_DEFAULT_PASSWORD=MySecurePassword123!
   
   # Run application
   streamlit run rcm_fmeca_app.py
   ```
   
   **Linux/Mac (Bash):**
   ```bash
   # Load from .env file
   export $(cat .env | xargs)
   
   # Or set manually
   export ADMIN_DEFAULT_PASSWORD=MySecurePassword123!
   
   # Run application
   streamlit run rcm_fmeca_app.py
   ```

### Option 2: Using System Environment Variables

**Windows:**
1. Open System Properties → Advanced → Environment Variables
2. Add new User Variable:
   - Name: `ADMIN_DEFAULT_PASSWORD`
   - Value: `YourSecurePassword`
3. Restart your terminal

**Linux/Mac:**
1. Add to `~/.bashrc` or `~/.zshrc`:
   ```bash
   export ADMIN_DEFAULT_PASSWORD="YourSecurePassword"
   ```
2. Reload: `source ~/.bashrc`

## Cloud Deployment

### Streamlit Community Cloud

1. **Deploy Your App:**
   - Push code to GitHub (sensitive files excluded by `.gitignore`)
   - Go to https://share.streamlit.io
   - Connect your GitHub repository

2. **Set Environment Variables:**
   - In Streamlit Cloud dashboard, go to your app
   - Click "⋮" menu → "Settings"
   - Go to "Secrets" section
   - Add your secrets in TOML format:
   
   ```toml
   # Streamlit secrets format
   ADMIN_DEFAULT_PASSWORD = "YourSecurePassword123!"
   ```

3. **Access in Code:**
   The app automatically loads these as environment variables.

### Heroku

1. **Set Config Vars:**
   ```bash
   heroku config:set ADMIN_DEFAULT_PASSWORD=YourSecurePassword123!
   ```

2. **Or via Dashboard:**
   - Go to App Settings
   - Click "Reveal Config Vars"
   - Add: `ADMIN_DEFAULT_PASSWORD` = `YourSecurePassword123!`

### AWS (EC2, Elastic Beanstalk)

**EC2:**
```bash
# SSH into instance
ssh user@your-ec2-instance

# Add to environment
echo 'export ADMIN_DEFAULT_PASSWORD="YourSecurePassword123!"' >> ~/.bashrc
source ~/.bashrc
```

**Elastic Beanstalk:**
```bash
# Using EB CLI
eb setenv ADMIN_DEFAULT_PASSWORD=YourSecurePassword123!
```

Or via AWS Console:
- Configuration → Software → Environment Properties
- Add: `ADMIN_DEFAULT_PASSWORD` = `YourSecurePassword123!`

### Google Cloud Platform (Cloud Run, App Engine)

**Cloud Run:**
```bash
gcloud run deploy rcm-fmeca \
  --image gcr.io/PROJECT_ID/rcm-fmeca \
  --set-env-vars ADMIN_DEFAULT_PASSWORD=YourSecurePassword123!
```

**App Engine (app.yaml):**
```yaml
env_variables:
  ADMIN_DEFAULT_PASSWORD: 'YourSecurePassword123!'
```

### Azure (App Service)

```bash
# Using Azure CLI
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name myApp \
  --settings ADMIN_DEFAULT_PASSWORD=YourSecurePassword123!
```

Or via Portal:
- App Service → Configuration → Application Settings
- Add new setting: `ADMIN_DEFAULT_PASSWORD`

### Docker

**Dockerfile:**
```dockerfile
# Don't hardcode secrets in Dockerfile!
# Pass at runtime instead
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  rcm-fmeca:
    build: .
    environment:
      - ADMIN_DEFAULT_PASSWORD=${ADMIN_DEFAULT_PASSWORD}
    env_file:
      - .env  # Load from .env file
```

**Docker Run:**
```bash
docker run -e ADMIN_DEFAULT_PASSWORD=YourSecurePassword123! rcm-fmeca
```

## GitHub Actions / CI/CD

### GitHub Secrets

1. **Add Repository Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `ADMIN_DEFAULT_PASSWORD`
   - Value: `YourSecurePassword123!`

2. **Use in Workflow (.github/workflows/deploy.yml):**
   ```yaml
   name: Deploy
   on:
     push:
       branches: [main]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Deploy to Streamlit Cloud
           env:
             ADMIN_DEFAULT_PASSWORD: ${{ secrets.ADMIN_DEFAULT_PASSWORD }}
           run: |
             # Your deployment commands
   ```

## Best Practices

### ✅ DO

1. **Use Strong Passwords in Production:**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Use password generators

2. **Different Passwords Per Environment:**
   - Development: Can use simple password
   - Staging: Use production-strength password
   - Production: Use strongest password

3. **Rotate Passwords Regularly:**
   - Update environment variables
   - Delete `.users.json` to force recreation with new password
   - Inform users of the change

4. **Document Required Variables:**
   - Keep `.env.example` updated
   - List all required variables in README

5. **Use Secret Management Services:**
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
   - HashiCorp Vault

### ❌ DON'T

1. **Never Hardcode Secrets:**
   ```python
   # BAD!
   password = "odyssey"
   
   # GOOD!
   password = os.getenv('ADMIN_DEFAULT_PASSWORD', 'odyssey')
   ```

2. **Never Commit `.env`:**
   - Always in `.gitignore`
   - Check before every commit: `git status`

3. **Never Share Secrets in Public:**
   - No secrets in GitHub Issues
   - No secrets in Pull Requests
   - No secrets in documentation

4. **Never Log Secrets:**
   ```python
   # BAD!
   print(f"Password: {password}")
   
   # GOOD!
   print("Password configured successfully")
   ```

## Verification

### Check Environment Variables Are Working

Add a startup message to verify (without exposing the actual value):

```python
# In rcm_fmeca_app.py
if __name__ == "__main__":
    # Check if custom password is set
    if os.getenv('ADMIN_DEFAULT_PASSWORD'):
        print("✓ Using custom admin password from environment")
    else:
        print("⚠ Using default admin password (consider setting ADMIN_DEFAULT_PASSWORD)")
```

### Test Different Environments

1. **Local Test:**
   ```bash
   # Unset variable
   unset ADMIN_DEFAULT_PASSWORD
   streamlit run rcm_fmeca_app.py
   # Should use default: odyssey
   
   # Set variable
   export ADMIN_DEFAULT_PASSWORD=TestPassword123!
   streamlit run rcm_fmeca_app.py
   # Should use: TestPassword123!
   ```

2. **Verify Password Hash:**
   ```python
   import hashlib
   password = "your_password"
   hash_value = hashlib.sha256(password.encode()).hexdigest()
   print(f"Expected hash: {hash_value}")
   # Compare with hash in .users.json
   ```

## Troubleshooting

### Environment Variable Not Loading

**Symptom:** Application still uses default password

**Solutions:**
1. Verify variable is set: `echo $ADMIN_DEFAULT_PASSWORD` (Linux/Mac) or `echo %ADMIN_DEFAULT_PASSWORD%` (Windows)
2. Restart terminal after setting system variables
3. Check for typos in variable name
4. Verify `.env` file format (no quotes needed for values)

### Can't Find .env File

**Symptom:** Variables not loading from .env

**Solutions:**
1. Ensure `.env` is in the same directory as `rcm_fmeca_app.py`
2. Check file name (not `.env.txt` or `env`)
3. On Windows, show file extensions to verify

### Wrong Password After Deployment

**Symptom:** Can't login with expected password

**Solutions:**
1. Delete `.users.json` on the server
2. Restart application to recreate with new password
3. Verify environment variable is set in cloud platform
4. Check logs for "Using custom admin password" message

## Migration from Hardcoded Values

If you've already deployed with hardcoded password:

1. **Update code** to use environment variables (already done ✓)
2. **Set environment variable** on all deployments
3. **Delete `.users.json`** from all environments
4. **Restart application** - will recreate with new password
5. **Test login** with new password
6. **Update documentation** with new default credentials

---

**Last Updated:** December 7, 2025  
**Version:** 1.0.2+

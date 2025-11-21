# 🔒 Security Best Practices

This document outlines security considerations for the Video Automation system.

---

## API Keys and Credentials

### Never Commit Sensitive Files

The following files contain sensitive information and should **NEVER** be committed to Git:

- ❌ `config.py` - Contains API keys
- ❌ `credentials.json` - OAuth client secrets
- ❌ `credentials_second.json` - Second account OAuth secrets
- ❌ `token.json` - OAuth access tokens
- ❌ `token_second.json` - Second account tokens
- ❌ `.env` - Environment variables

✅ These files are already in `.gitignore`

### Verify Before Pushing

Before pushing to GitHub, always check:

```bash
# Check what files will be committed
git status

# Make sure no sensitive files are listed
git diff --cached
```

---

## API Key Management

### Rotate Keys Regularly

**Recommended rotation schedule**:
- OAuth credentials: Every 90 days
- API keys: Every 30-90 days

### How to Rotate

**Google Gemini API Key**:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Update `config.py`
4. Delete the old key

**OpenAI API Key**:
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new key
3. Update `config.py`
4. Revoke the old key

**OAuth Credentials**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new OAuth credentials
3. Download new `credentials.json`
4. Delete `token.json` and re-authenticate

---

## OAuth Scopes

### Understanding Scopes

The application requests these OAuth scopes:

```python
SCOPES = [
    'https://www.googleapis.com/auth/drive',           # Full Drive access
    'https://www.googleapis.com/auth/youtube.upload',  # YouTube upload
    'https://www.googleapis.com/auth/spreadsheets'     # Sheets access
]
```

### Why These Scopes?

- **Drive**: Read files, move files to Done folder
- **YouTube**: Upload videos, set thumbnails
- **Sheets**: Write log entries

### Minimize Scope Access

If you want to restrict permissions:

1. **Read-only Drive** (if not moving files):
   ```python
   'https://www.googleapis.com/auth/drive.readonly'
   ```

2. **Specific folder access**: Share only specific folders with the service account

---

## Data Privacy

### What Data is Processed?

- **Video files**: Downloaded temporarily, deleted after upload
- **Thumbnails**: Generated temporarily, deleted after upload
- **Metadata**: Video titles, descriptions sent to AI services

### Where is Data Sent?

- **Google Gemini**: Video content for analysis
- **OpenAI DALL-E**: Thumbnail prompts (text only, not video)
- **YouTube**: Video files and metadata
- **Google Sheets**: Upload logs (titles, links, timestamps)

### Data Retention

- **Local**: Videos and thumbnails deleted after processing
- **Google Drive**: Videos moved to Done folder (you control retention)
- **YouTube**: Videos remain until you delete them
- **Sheets**: Logs remain until you delete them

---

## Network Security

### Use HTTPS

All API calls use HTTPS by default. Never disable SSL verification.

### Firewall Considerations

The application needs outbound access to:
- `*.googleapis.com` (Google APIs)
- `api.openai.com` (OpenAI)
- `*.google.com` (OAuth)

### VPN Compatibility

The application works with VPNs. No special configuration needed.

---

## Production Deployment

### Environment Variables

For production, use environment variables instead of hardcoded values:

```python
# config.py
import os

class Config:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    # ... etc
```

Set variables:
```bash
export GEMINI_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

### Use Secrets Management

For cloud deployments:
- **Google Cloud**: Use Secret Manager
- **AWS**: Use Secrets Manager or Parameter Store
- **Azure**: Use Key Vault

### Docker Security

If using Docker:

```dockerfile
# Don't include sensitive files in image
# Use .dockerignore
config.py
credentials.json
token.json
*.env
```

Mount secrets at runtime:
```bash
docker run -v /path/to/credentials.json:/app/credentials.json ...
```

---

## Rate Limiting

### API Quotas

Respect API quotas to avoid service disruption:

- **YouTube**: 10,000 units/day (free tier)
- **Gemini**: Varies by tier
- **OpenAI**: Varies by tier

### Implement Backoff

The application includes retry logic with exponential backoff. Don't disable it.

---

## Monitoring

### Log Sensitive Operations

Monitor for:
- Failed authentication attempts
- API quota warnings
- Unusual upload patterns

### Set Up Alerts

Configure alerts for:
- API quota approaching limit
- Authentication failures
- Upload errors

---

## Incident Response

### If API Key is Compromised

1. **Immediately revoke** the compromised key
2. **Generate a new key**
3. **Update configuration**
4. **Review recent activity** for unauthorized usage
5. **Check billing** for unexpected charges

### If OAuth Token is Compromised

1. **Revoke access** in [Google Account Settings](https://myaccount.google.com/permissions)
2. **Delete** `token.json`
3. **Re-authenticate** with `python authenticate.py`
4. **Review YouTube uploads** for unauthorized videos

---

## Compliance

### GDPR Considerations

If processing videos containing personal data:
- Ensure you have consent to process the data
- Implement data retention policies
- Provide data deletion capabilities
- Document data processing activities

### YouTube Terms of Service

Ensure your usage complies with:
- [YouTube Terms of Service](https://www.youtube.com/t/terms)
- [YouTube API Services Terms](https://developers.google.com/youtube/terms/api-services-terms-of-service)

---

## Security Checklist

Before deploying to production:

- [ ] All sensitive files in `.gitignore`
- [ ] API keys stored securely (not hardcoded)
- [ ] OAuth credentials rotated regularly
- [ ] Monitoring and alerts configured
- [ ] Rate limiting respected
- [ ] Data retention policy defined
- [ ] Incident response plan documented
- [ ] Terms of Service compliance verified

---

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email the maintainer directly
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We'll respond within 48 hours.

---

## Additional Resources

- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [OpenAI API Security](https://platform.openai.com/docs/guides/safety-best-practices)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

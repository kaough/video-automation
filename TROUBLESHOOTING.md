# 🔧 Troubleshooting Guide

Common issues and solutions for the Video Automation system.

---

## Authentication Issues

### Error: "Access blocked: App has not completed verification"

**Cause**: Your OAuth app is in testing mode and the user isn't added as a test user.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **OAuth consent screen**
3. Scroll to **Test users**
4. Click **+ ADD USERS**
5. Add your Google account email
6. Click **Save**
7. Delete `token.json` and run `python authenticate.py` again

---

### Error: "Invalid grant" or "Token has been expired or revoked"

**Cause**: Your OAuth token is no longer valid.

**Solution**:
```bash
# Delete the old token
rm token.json

# Re-authenticate
python authenticate.py
```

---

### Browser doesn't open during authentication

**Cause**: The script can't automatically open your browser.

**Solution**:
1. Copy the URL shown in the terminal
2. Paste it into your browser manually
3. Complete the authentication
4. Copy the authorization code
5. Paste it back into the terminal

---

## File Detection Issues

### "No new files found" but files exist in Drive folder

**Possible causes and solutions**:

1. **Wrong folder ID**
   - Verify the folder ID in `config.py` matches your Drive folder
   - URL format: `drive.google.com/drive/folders/FOLDER_ID`

2. **Permission issues**
   - Make sure the authenticated account has access to the folder
   - Share the folder with your Google account (Editor permission)

3. **Wrong file extension**
   - Supported formats: `.mp4`, `.mov`, `.m4v`
   - Check your video file extension

4. **Files already processed**
   - Check your "Done" folder - files may have been moved there
   - The script moves processed files automatically

**Debug command**:
```bash
python check_drive_files.py
```

This will show all files in your folder and which ones are recognized as videos.

---

## API Errors

### "Quota exceeded" errors

**Cause**: You've hit the daily API quota limit.

**YouTube API Quota**:
- Free tier: 10,000 units/day
- Each upload: ~1,600 units
- Limit: ~6 uploads/day

**Solutions**:
1. Wait 24 hours for quota to reset
2. Request quota increase from Google Cloud Console
3. Reduce upload frequency

---

### "Invalid API key" errors

**Cause**: API key is incorrect or doesn't have proper permissions.

**Solution**:
1. Verify API keys in `config.py`
2. For Gemini: Check [Google AI Studio](https://aistudio.google.com/app/apikey)
3. For OpenAI: Check [OpenAI Platform](https://platform.openai.com/api-keys)
4. Make sure there are no extra spaces or quotes

---

## Video Processing Issues

### Video compression fails

**Cause**: FFmpeg not installed or video file corrupted.

**Solution**:
1. Install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`
2. Add FFmpeg to your system PATH
3. Restart the script

---

### Thumbnail generation fails

**Possible causes**:

1. **OpenAI API key invalid**
   - Verify your API key in `config.py`
   - Check you have credits in your OpenAI account

2. **Network issues**
   - Check your internet connection
   - Try again in a few minutes

3. **DALL-E API down**
   - Check [OpenAI Status](https://status.openai.com/)

**Workaround**: Comment out thumbnail generation in `main.py` (line 71-72)

---

## Upload Issues

### YouTube upload fails with "Forbidden"

**Cause**: YouTube API not enabled or OAuth scopes missing.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **YouTube Data API v3**
3. Delete `token.json`
4. Run `python authenticate.py` again
5. Make sure to grant all permissions

---

### Google Sheets logging fails

**Cause**: Spreadsheet ID wrong or permissions missing.

**Solution**:
1. Verify `SPREADSHEET_ID` in `config.py`
2. Make sure the spreadsheet exists
3. Share the spreadsheet with your Google account
4. Check Google Sheets API is enabled

---

## Configuration Issues

### "Module 'config' has no attribute"

**Cause**: `config.py` is missing required fields.

**Solution**:
1. Compare your `config.py` with `config.example.py`
2. Make sure all required fields are present
3. Run `python validate_setup.py` to check

---

### Import errors

**Cause**: Dependencies not installed.

**Solution**:
```bash
pip install -r requirements.txt
```

---

## Performance Issues

### Script is slow

**Possible causes**:

1. **Large video files**
   - Compression takes time for large files
   - Consider pre-compressing videos

2. **Slow internet**
   - Upload speed affects YouTube upload time
   - Check your internet connection

3. **AI API latency**
   - Gemini and DALL-E can take 10-30 seconds
   - This is normal

---

## General Debugging

### Enable verbose logging

Add this to the top of `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Python version

```bash
python --version
```

Required: Python 3.12+

### Verify all files exist

```bash
python validate_setup.py
```

---

## Still Having Issues?

1. **Check the FAQ**: See [FAQ.md](FAQ.md)
2. **Search existing issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/video-automation/issues)
3. **Create a new issue**: Include:
   - Error message (full traceback)
   - Python version
   - Operating system
   - Steps to reproduce

---

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `FileNotFoundError: credentials.json` | Missing OAuth credentials | Download from Google Cloud Console |
| `ModuleNotFoundError: google` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `KeyError: 'DRIVE_FOLDER_ID'` | config.py incomplete | Run `python setup_wizard.py` |
| `HttpError 403` | Permission denied | Check folder sharing and API scopes |
| `HttpError 404` | Resource not found | Verify folder/spreadsheet IDs |
| `HttpError 429` | Rate limit exceeded | Wait and try again later |

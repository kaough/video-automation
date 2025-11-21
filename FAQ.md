# ❓ Frequently Asked Questions (FAQ)

---

## General Questions

### What does this automation do?

The Video Automation system:
1. Monitors a Google Drive folder for new videos
2. Analyzes video content with Google Gemini AI
3. Generates custom thumbnails with DALL-E 3
4. Uploads videos to YouTube with AI-generated metadata
5. Logs all uploads to Google Sheets
6. Moves processed videos to a "Done" folder

### How much does it cost to run?

**Per video costs** (approximate):
- Google Gemini analysis: ~$0.01
- DALL-E 3 thumbnail: $0.04
- **Total: ~$0.05 per video**

**Free tier limits**:
- Google Drive API: Free (1B queries/day)
- YouTube API: Free (10,000 units/day ≈ 6 uploads)
- Google Sheets API: Free (500 requests/100s)

### Can I use this commercially?

Yes! The project is MIT licensed. You can use it for personal or commercial purposes. However, you're responsible for:
- Your own API costs
- Compliance with YouTube's Terms of Service
- Content ownership and copyright

---

## Setup Questions

### Do I need a credit card?

- **Google Cloud**: No credit card required for free tier
- **OpenAI**: Yes, credit card required (but you get free credits initially)
- **Google Gemini**: No credit card required for free tier

### Can I use this without OpenAI?

Not currently - DALL-E 3 is required for thumbnail generation. However, you could:
1. Disable thumbnail generation (comment out lines 69-71 in `main.py`)
2. Use pre-made thumbnails
3. Contribute code to support alternative thumbnail generators!

### What Google account should I use?

Use the Google account that:
- Owns your YouTube channel
- Has access to your Google Drive folders
- You want to use for Google Sheets logging

---

## Video Questions

### What video formats are supported?

Supported formats:
- `.mp4` (recommended)
- `.mov`
- `.m4v`

To add more formats, edit `VIDEO_EXTENSIONS` in `config.py`.

### What's the maximum video size?

- **YouTube limit**: 256 GB or 12 hours
- **Practical limit**: Depends on your upload speed

The script includes automatic compression for large files.

### Can I process multiple videos at once?

The script processes videos one at a time in the order they appear in the folder. To process multiple videos:
1. Upload all videos to the monitored folder
2. The script will process them sequentially

### How long does processing take?

**Typical timeline per video**:
- Download: 1-5 minutes (depends on size)
- Compression: 2-10 minutes (if needed)
- AI analysis: 30-60 seconds
- Thumbnail generation: 10-30 seconds
- Upload to YouTube: 2-10 minutes (depends on size)

**Total**: 5-30 minutes per video

---

## YouTube Questions

### What privacy settings are used?

Default: `public`

To change, edit `YOUTUBE_PRIVACY_STATUS` in `config.py`:
- `public` - Anyone can see
- `unlisted` - Only people with the link
- `private` - Only you can see

### Can I customize the video category?

Yes! Edit `YOUTUBE_CATEGORY_ID` in `config.py`.

Common categories:
- `22` - People & Blogs (default)
- `20` - Gaming
- `24` - Entertainment
- `28` - Science & Technology

[Full list of category IDs](https://developers.google.com/youtube/v3/docs/videoCategories/list)

### Can I upload to multiple YouTube channels?

Yes! See the "Dual Upload" section in `SETUP.md`. You'll need:
- Two sets of OAuth credentials
- Two YouTube channels
- Set `ENABLE_DUAL_UPLOAD = True` in `config.py`

### How are titles and descriptions generated?

The AI (Google Gemini) analyzes your video and generates:
- **Title**: SEO-optimized, ≤60 characters
- **Description**: Engaging summary with relevant hashtags
- **Thumbnail prompt**: Description for DALL-E to create a custom thumbnail

---

## Technical Questions

### Can I run this on a server?

Yes! Options:
1. **Google Cloud Run** (recommended for cloud)
2. **AWS EC2** or similar VPS
3. **Raspberry Pi** (for local server)

For server deployment:
- Use environment variables for config
- Set up proper logging
- Consider using Docker (Dockerfile included)

### Can I schedule it to run automatically?

Yes! Options:

**Windows**:
```powershell
# Task Scheduler
schtasks /create /tn "Video Automation" /tr "python C:\path\to\main.py" /sc daily /st 09:00
```

**Mac/Linux**:
```bash
# Cron job (runs every hour)
0 * * * * cd /path/to/video-automation && python main.py
```

**Cloud**: Use Cloud Scheduler with Cloud Run

### How do I stop the script?

Press `Ctrl+C` in the terminal where it's running.

### Can I customize the AI prompts?

Yes! Edit the prompts in `services/ai_service.py`:
- Line ~30: Video analysis prompt
- Line ~60: Thumbnail generation prompt

---

## Troubleshooting Questions

### Why isn't my video being detected?

Common causes:
1. Wrong folder ID in `config.py`
2. File extension not supported
3. Permission issues
4. Video already processed and moved

Run `python check_drive_files.py` to debug.

### Authentication keeps failing

Try:
1. Delete `token.json`
2. Run `python authenticate.py` again
3. Make sure you're added as a test user in Google Cloud Console

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more details.

### How do I reset everything?

```bash
# Delete authentication tokens
rm token.json token_second.json

# Delete configuration
rm config.py

# Re-run setup wizard
python setup_wizard.py
```

---

## Feature Requests

### Can you add [feature]?

We welcome contributions! Please:
1. Check existing [GitHub Issues](https://github.com/YOUR_USERNAME/video-automation/issues)
2. Create a new issue describing the feature
3. Or submit a Pull Request!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Planned features?

See the "Future Enhancements" section in [README.md](README.md).

---

## Still have questions?

- 📖 Read the [Setup Guide](SETUP.md)
- 🔧 Check [Troubleshooting](TROUBLESHOOTING.md)
- 💬 Open an issue on [GitHub](https://github.com/YOUR_USERNAME/video-automation/issues)

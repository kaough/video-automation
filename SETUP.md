# 🚀 Complete Setup Guide

This guide will walk you through setting up the AI Video Automation system from scratch. Follow each step carefully.

## Prerequisites

- **Python 3.12+** installed
- A **Google account**
- A **YouTube channel**
- Credit card for API services (most have free tiers)

## Estimated Setup Time

⏱️ **30-45 minutes** for first-time setup

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/video-automation.git
cd video-automation
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Google Cloud Project Setup

### 3.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter a project name (e.g., "Video Automation")
4. Click **"Create"**

### 3.2 Enable Required APIs

Enable these APIs in your project:

1. Go to **APIs & Services** → **Library**
2. Search for and enable each of these:
   - ✅ **Google Drive API**
   - ✅ **YouTube Data API v3**
   - ✅ **Google Sheets API**

### 3.3 Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. If prompted, configure the **OAuth consent screen**:
   - User Type: **External**
   - App name: `Video Automation`
   - User support email: Your email
   - Developer contact: Your email
   - Click **"Save and Continue"**
   - Scopes: Skip this, click **"Save and Continue"**
   - Test users: Add your Google account email
   - Click **"Save and Continue"**
4. Back to creating OAuth client ID:
   - Application type: **Desktop app**
   - Name: `Video Automation Desktop`
   - Click **"Create"**
5. Click **"Download JSON"**
6. Rename the downloaded file to `credentials.json`
7. Move it to your project folder

---

## Step 4: Get API Keys

### 4.1 Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Select your Google Cloud project
4. Copy the API key (save it for later)

### 4.2 OpenAI API Key (for DALL-E 3)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click **"Create new secret key"**
4. Name it `Video Automation`
5. Copy the API key (save it for later)

> [!WARNING]
> Keep your API keys secret! Never commit them to Git or share them publicly.

---

## Step 5: Google Drive Setup

### 5.1 Create Folders

1. Go to [Google Drive](https://drive.google.com/)
2. Create two folders:
   - **"Videos to Process"** (for new videos)
   - **"Done"** (for processed videos)

### 5.2 Get Folder IDs

For each folder:
1. Open the folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Copy the `FOLDER_ID_HERE` part
4. Save both IDs for later

---

## Step 6: Google Sheets Setup

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it `Video Automation Log`
4. Look at the URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
5. Copy the `SPREADSHEET_ID` part
6. Save it for later

---

## Step 7: Configure the Application

### Option A: Use the Setup Wizard (Recommended)

Run the interactive setup wizard:

```bash
python setup_wizard.py
```

Follow the prompts to enter all your API keys and folder IDs.

### Option B: Manual Configuration

1. Copy the example config:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` and fill in:
   - `DRIVE_FOLDER_ID` - Your "Videos to Process" folder ID
   - `DRIVE_DONE_FOLDER_ID` - Your "Done" folder ID
   - `GEMINI_API_KEY` - Your Google Gemini API key
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `SPREADSHEET_ID` - Your Google Sheets ID

---

## Step 8: Authenticate with Google

Run the authentication script:

```bash
python authenticate.py
```

A browser window will open:
1. Sign in with your Google account
2. Click **"Allow"** for all permissions
3. Wait for "Authentication successful" message

---

## Step 9: Validate Your Setup

Run the validation script:

```bash
python validate_setup.py
```

This will check:
- ✅ All required files exist
- ✅ Configuration is valid
- ✅ API keys work
- ✅ Google Drive access works
- ✅ YouTube access works
- ✅ Google Sheets access works

Fix any errors before proceeding.

---

## Step 10: Test with a Video

1. Upload a test video to your "Videos to Process" folder
2. Run the automation:
   ```bash
   python main.py
   ```
3. Watch the console output
4. Check YouTube for your uploaded video!

---

## 🎉 Success!

Your automation is now running! It will:
- Monitor your Google Drive folder every 60 seconds
- Process new videos automatically
- Upload to YouTube with AI-generated metadata
- Log everything to Google Sheets

---

## Next Steps

- Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Check [FAQ.md](FAQ.md) for frequently asked questions
- See [README.md](README.md) for feature details

---

## Need Help?

- 📖 Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- 💬 Open an issue on GitHub
- 📧 Contact the maintainer

---

## Cost Considerations

### Free Tiers
- **Google Drive API**: Free up to 1 billion queries/day
- **YouTube API**: Free up to 10,000 quota units/day (~6 uploads)
- **Google Sheets API**: Free up to 500 requests/100 seconds

### Paid Services
- **Google Gemini**: ~$0.01 per video analysis
- **OpenAI DALL-E 3**: $0.04 per thumbnail (1024x1024)

**Estimated cost per video**: ~$0.05

> [!TIP]
> Start with a few test videos to understand costs before automating at scale.

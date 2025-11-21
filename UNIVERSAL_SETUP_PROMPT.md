# 🚀 Universal Setup System Prompt

Use this prompt with an AI assistant to transform any project into a universal, user-friendly, GitHub-ready tool.

---

## The Prompt

```
I want to make my [PROJECT_NAME] project universal and accessible for anyone to use with their own accounts/API keys. Currently, it's configured with my personal credentials.

Please create a comprehensive setup system that includes:

## 1. Documentation Files

Create these markdown files:

### SETUP.md
- Complete step-by-step setup guide from scratch
- How to obtain all required API keys/credentials
- How to configure the application
- Cost estimates (if applicable)
- Troubleshooting common setup issues
- Estimated setup time

### TROUBLESHOOTING.md
- Common issues organized by category
- Clear problem descriptions
- Root causes
- Step-by-step solutions
- Debug commands
- Error message reference table

### FAQ.md
- General questions about the project
- Setup and configuration questions
- Technical questions
- Cost/pricing questions
- Feature-specific questions
- Links to other documentation

### SECURITY.md
- API key management best practices
- Credential rotation guidelines
- Data privacy considerations
- Production deployment security
- Incident response procedures
- Compliance considerations (GDPR, etc.)

### CONTRIBUTING.md
- How to contribute (code, docs, bug reports)
- Development setup instructions
- Code style guidelines
- Pull request process
- Bug report template
- Feature request template
- Community guidelines

## 2. Setup Scripts

Create these Python scripts:

### setup_wizard.py
Interactive setup wizard that:
- Checks system requirements (Python version, etc.)
- Validates required files exist
- Guides user through configuration
- Installs dependencies
- Runs authentication flow
- Provides colored terminal output
- Handles errors gracefully

### validate_setup.py
Validation script that:
- Checks all required files exist
- Validates configuration completeness
- Tests API connectivity
- Provides detailed error messages
- Suggests fixes for common issues
- Returns clear success/failure status

### authenticate.py (if applicable)
Helper script for OAuth/API authentication

## 3. Configuration Updates

### Update config.example.py (or equivalent)
- Add detailed comments for each field
- Include examples of where to find values
- Mark required vs optional fields
- Add links to relevant documentation
- Support environment variables

### Verify .gitignore
Ensure it excludes:
- Configuration files with secrets
- API keys and tokens
- OAuth credentials
- Any generated files with sensitive data
- Local environment files

## 4. README.md Enhancement

Update README.md to include:
- Badges (Python version, license, etc.)
- Clear "For New Users" callout linking to SETUP.md
- Quick Start section (separate paths for new vs experienced users)
- Documentation links section
- Cost estimate (if applicable)
- Clear prerequisites with setup guide link
- Simplified installation instructions

## 5. Additional Requirements

- All scripts should have colored terminal output for better UX
- Include progress indicators where applicable
- Provide clear error messages with actionable solutions
- Make everything work cross-platform (Windows, Mac, Linux)
- Add helpful debug/diagnostic tools
- Ensure all sensitive files are gitignored

## 6. Verification

After creating everything:
- Test the setup wizard end-to-end
- Verify validation script catches common errors
- Ensure all documentation links work
- Check that .gitignore excludes all sensitive files
- Confirm README renders well on GitHub

## Project Context

[Provide details about your project]:
- What it does
- What APIs/services it uses
- What credentials are needed
- Current configuration method
- Target audience

Please create all files following best practices for open-source projects.
```

---

## How to Use This Prompt

1. **Copy the prompt above**
2. **Replace `[PROJECT_NAME]` with your actual project name**
3. **Fill in the "Project Context" section** with details about your specific project
4. **Paste into your AI assistant** (Claude, ChatGPT, Gemini, etc.)
5. **Review and customize** the generated files as needed

---

## Example Project Context

For the video automation project, the context was:

```
Project Context:
- What it does: Monitors Google Drive for videos, analyzes them with AI, generates thumbnails, uploads to YouTube
- What APIs/services it uses: Google Drive API, YouTube API, Google Sheets API, Google Gemini, OpenAI DALL-E 3
- What credentials are needed: Google OAuth credentials, Gemini API key, OpenAI API key, Drive folder IDs, Sheets ID
- Current configuration method: Hardcoded in config.py
- Target audience: Content creators, YouTube channel managers, automation enthusiasts
```

---

## Expected Output

The AI will create:
- ✅ 5-7 comprehensive documentation files
- ✅ 3-5 setup/helper scripts
- ✅ Updated README.md with badges and clear structure
- ✅ Enhanced configuration files with comments
- ✅ Verified .gitignore for security

---

## Customization Tips

### For Different Project Types

**Web Applications:**
- Add deployment guides (Vercel, Netlify, etc.)
- Include environment variable setup
- Add database migration instructions

**CLI Tools:**
- Add installation via pip/npm
- Include shell completion setup
- Add usage examples

**APIs/Libraries:**
- Add API reference documentation
- Include code examples
- Add testing instructions

### For Different Languages

**Node.js:**
- Replace `setup_wizard.py` with `setup-wizard.js`
- Use `package.json` instead of `requirements.txt`
- Adapt for npm/yarn

**Go:**
- Use `go.mod` for dependencies
- Adapt scripts to Go conventions
- Include build instructions

**Rust:**
- Use `Cargo.toml` for dependencies
- Include compilation instructions
- Add platform-specific notes

---

## Tips for Success

1. **Be specific** about your project in the context section
2. **Review generated files** - AI may need guidance on project-specific details
3. **Test the setup wizard** with a fresh clone of your repo
4. **Get feedback** from a friend trying to set it up
5. **Iterate** based on real user experience

---

## What Makes This Effective

✅ **Comprehensive** - Covers all aspects of user onboarding  
✅ **User-focused** - Prioritizes ease of setup  
✅ **Secure** - Emphasizes security best practices  
✅ **Maintainable** - Clear contribution guidelines  
✅ **Professional** - GitHub-ready documentation  

---

## License

This prompt template is public domain. Use it for any project!

---

## Credits

Created for the AI Video Automation project as a template for making any project universal and accessible.

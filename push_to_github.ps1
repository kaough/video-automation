# GitHub Push Script
# Run this in a NEW PowerShell window

Write-Host "=== GitHub Push Script ===" -ForegroundColor Green
Write-Host ""

# Navigate to project directory
Set-Location "c:\Users\dkaough\Documents\ai stuff\video_automation"

# Check if Git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git config user.name "kaough"
    git config user.email "dkaough@users.noreply.github.com"
}

# Add all files
Write-Host "Adding files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: AI-powered YouTube automation with DALL-E 3"

# Add remote if not exists
$remoteExists = git remote | Select-String "origin"
if (-not $remoteExists) {
    Write-Host "Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/kaough/ai-video-automation.git
}

# Set branch to main
Write-Host "Setting branch to main..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Green
Write-Host "You will be prompted to log in to GitHub in your browser." -ForegroundColor Cyan
Write-Host ""

git push -u origin main

Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Green
Write-Host "Check your repository at: https://github.com/kaough/ai-video-automation" -ForegroundColor Cyan

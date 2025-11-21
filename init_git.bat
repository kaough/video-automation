@echo off
echo Initializing Git repository...
cd /d "c:\Users\dkaough\Documents\ai stuff\video_automation"

if exist ".git" (
    echo Git repository already exists!
) else (
    git init
    git config user.name "kaough"
    git config user.email "dkaough@users.noreply.github.com"
    git add .
    git commit -m "Initial commit: AI video automation"
    git branch -M main
    echo Git repository initialized!
)

echo.
echo Now open GitHub Desktop and:
echo 1. Click File -^> Add local repository
echo 2. Browse to: c:\Users\dkaough\Documents\ai stuff\video_automation
echo 3. Click Add Repository
echo 4. Click Publish Repository
echo.
pause

@echo off
echo === Pushing to GitHub ===
echo.

cd /d "c:\Users\dkaough\Documents\ai stuff\video_automation"

"C:\Program Files\Git\cmd\git.exe" init
"C:\Program Files\Git\cmd\git.exe" config user.name "kaough"
"C:\Program Files\Git\cmd\git.exe" config user.email "dkaough@users.noreply.github.com"
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Initial commit: AI video automation"
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/kaough/ai-video-automation.git
"C:\Program Files\Git\cmd\git.exe" push -u origin main

echo.
echo === Done! ===
echo Check: https://github.com/kaough/ai-video-automation
pause

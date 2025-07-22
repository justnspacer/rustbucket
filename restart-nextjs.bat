@echo off
echo =======================================
echo   Next.js Restart (Config Changes)
echo =======================================
echo.

echo Stopping Next.js development server...
taskkill /F /IM "node.exe" /FI "COMMANDLINE==*next-server*" 2>nul
taskkill /F /IM "node.exe" /FI "COMMANDLINE==*next dev*" 2>nul

echo.
echo Starting Next.js with updated configuration...
cd /d "c:\Users\justn\code\rustbucket\next-rusty-tech"
start "Next.js App" cmd /k "npm run dev"

echo.
echo =======================================
echo   Next.js restarted with proxy routes!
echo =======================================
echo.
echo The proxy route is now available:
echo   /api/gateway/spotify/auth/profile
echo   -^> http://localhost:8000/api/spotify/auth/profile
echo.
echo Visit: http://localhost:3000/spotify
echo Click "Show Connection Test" to debug
echo.
pause

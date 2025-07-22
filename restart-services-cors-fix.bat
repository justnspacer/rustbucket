@echo off
echo ======================================
echo    CORS Fix Applied - Restart Services
echo ======================================
echo.

echo Stopping any running services...
taskkill /F /IM "uvicorn.exe" 2>nul
taskkill /F /IM "python.exe" /FI "WINDOWTITLE eq *spotify*" 2>nul

echo.
echo Starting Gatekeeper with CORS support...
cd /d "c:\Users\justn\code\rustbucket\gatekeeper"
start "Gatekeeper" cmd /k "uvicorn main:app --reload --port 8000"

echo.
echo Starting Spotify App...
cd /d "c:\Users\justn\code\rustbucket\spotify"
start "Spotify App" cmd /k "python run.py"

echo.
echo Services are starting...
echo - Gatekeeper: http://localhost:8000
echo - Spotify App: http://localhost:5000
echo.
echo You can now start your Next.js app:
echo   cd next-rusty-tech
echo   npm run dev
echo.
echo ======================================
echo    CORS should now be resolved!
echo ======================================
pause

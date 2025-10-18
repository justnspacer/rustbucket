@echo off
REM Debug helper script - runs parser test
echo Testing PDF Parser...
echo.
.venv\Scripts\python.exe test_parser.py
echo.
echo Press any key to exit...
pause > nul

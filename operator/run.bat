@echo off
REM Operator Service Runner for Windows
REM This script helps you run the Operator service with proper environment setup

echo ==================================
echo    Operator Service Launcher
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv_operator\" (
    echo Error: Virtual environment not found!
    echo Please create it with: python -m venv venv_operator
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo Please edit .env with your configuration before running.
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_operator\Scripts\activate.bat

REM Install/upgrade dependencies
echo Checking dependencies...
pip install -q -r requirements.txt

REM Run based on argument
if "%1"=="app" (
    echo Starting Flask webhook server...
    python app.py
) else if "%1"=="test" (
    echo Running command tests...
    python test_commands.py
) else if "%1"=="test-monitors" (
    echo Running monitor tests...
    python test_monitors.py
) else if "%1"=="send-sms" (
    echo Sending test SMS...
    python main.py
) else (
    echo Usage: run.bat [command]
    echo.
    echo Commands:
    echo   app            - Start the Flask webhook server
    echo   test           - Test command processor
    echo   test-monitors  - Test monitoring integrations
    echo   send-sms       - Send a test SMS
    echo.
    echo Example: run.bat app
    exit /b 1
)

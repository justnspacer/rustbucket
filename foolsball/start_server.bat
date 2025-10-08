@echo off
echo Starting NFL Teams Dashboard Server...
echo.
echo Activating virtual environment...
call venv_foolsball\Scripts\activate
echo.
echo Starting Flask server at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

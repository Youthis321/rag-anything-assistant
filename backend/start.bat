@echo off
echo Starting RAG Anything Assistant Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env has API key
findstr /C:"your_gemini_api_key_here" .env >nul
if %errorlevel% == 0 (
    echo.
    echo =================== IMPORTANT ===================
    echo Please edit .env file and add your Gemini API key
    echo Visit: https://makersuite.google.com/app/apikey
    echo Replace "your_gemini_api_key_here" with your actual key
    echo ================================================
    echo.
    pause
)

REM Start the application
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python app.py

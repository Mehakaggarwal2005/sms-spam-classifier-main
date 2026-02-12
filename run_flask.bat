@echo off
REM SMS Spam Detector - Flask Launcher
REM This script sets up and runs the Flask app on Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   SMS Spam Detector - Flask Launcher                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Download NLTK data
echo 📚 Downloading NLTK data...
python -m nltk.downloader punkt_tab punkt stopwords -d C:\Users\%USERNAME%\nltk_data
if errorlevel 1 (
    echo ⚠️  Warning: Could not download NLTK data automatically
    echo You may need to run: python -m nltk.downloader punkt_tab punkt stopwords
)

echo ✅ NLTK data ready
echo.

REM Run Flask
echo 🚀 Starting Flask app...
echo.
echo Opening browser at http://localhost:5000
echo Press Ctrl+C in this window to stop the server
echo.

python flask_app.py

pause

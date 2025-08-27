@echo off
REM EPUB to Audiobook Converter - Windows Installation Script
REM This script installs all required dependencies

echo ===================================================
echo EPUB to Audiobook Converter - Installation Script
echo ===================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python is installed
python --version

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo To get started:
echo 1. Place your EPUB files in the 'input' folder
echo 2. Run: python main.py -i input/your_book.epub
echo 3. Check the 'output' folder for your audiobook
echo.
echo For help: python main.py --help
echo For examples: python examples.py
echo.
echo Optional: Install GPU support for faster processing
echo   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
echo.
pause

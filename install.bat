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

REM Check Python version for TTS compatibility
for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYTHON_VERSION=%%i
echo Detected Python version: %PYTHON_VERSION%

REM Check if Python version is 3.12 or higher
for /f "tokens=*" %%i in ('python -c "import sys; print('high' if sys.version_info >= (3, 12) else 'ok')"') do set VERSION_CHECK=%%i

if "%VERSION_CHECK%"=="high" (
    echo WARNING: Python 3.12+ detected. TTS library may not be compatible.
    echo Installing basic dependencies only...
    pip install -r requirements-basic.txt
    
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install basic dependencies
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
    
    echo.
    echo NOTE: For full TTS functionality, consider using Python 3.8-3.11
    echo You can still use the demo version: python demo.py
) else (
    echo Installing full dependencies...
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install full dependencies
        echo Trying basic dependencies as fallback...
        pip install -r requirements-basic.txt
        
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to install basic dependencies
            echo Please check your internet connection and try again
            pause
            exit /b 1
        )
    )
)

echo.
echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo To get started:
echo 1. Place your EPUB files in the 'input' folder

REM Check Python version again for instructions
for /f "tokens=*" %%i in ('python -c "import sys; print('high' if sys.version_info >= (3, 12) else 'ok')"') do set VERSION_CHECK2=%%i
if "%VERSION_CHECK2%"=="high" (
    echo 2. Try demo first: python demo.py -i input/your_book.epub
    echo 3. For full conversion, use Python 3.8-3.11 or try: python main.py -i input/your_book.epub
) else (
    echo 2. Run: python main.py -i input/your_book.epub
)
echo 4. Check the 'output' folder for your audiobook
echo.
echo For help: python main.py --help
echo For examples: python examples.py
echo.
echo Optional: Install GPU support for faster processing
echo   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
echo.
pause

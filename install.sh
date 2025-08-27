#!/bin/bash
# EPUB to Audiobook Converter - Unix/Linux/macOS Installation Script
# This script installs all required dependencies

echo "==================================================="
echo "EPUB to Audiobook Converter - Installation Script"
echo "==================================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python 3.8 or higher"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python is installed"
$PYTHON_CMD --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "ERROR: pip is not installed"
        echo "Please install pip"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo
echo "Installing Python dependencies..."

# Check Python version for TTS compatibility
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Detected Python version: $PYTHON_VERSION"

# Check if Python version is 3.12 or higher
PYTHON_VERSION_CHECK=$($PYTHON_CMD -c "import sys; print('high' if sys.version_info >= (3, 12) else 'ok')")

if [ "$PYTHON_VERSION_CHECK" = "high" ]; then
    echo "WARNING: Python 3.12+ detected. TTS library may not be compatible."
    echo "Installing basic dependencies only..."
    $PIP_CMD install -r requirements-basic.txt
    
    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Failed to install basic dependencies"
        echo "Please check your internet connection and try again"
        exit 1
    fi
    
    echo ""
    echo "NOTE: For full TTS functionality, consider using Python 3.8-3.11"
    echo "You can still use the demo version: $PYTHON_CMD demo.py"
else
    echo "Installing full dependencies..."
    $PIP_CMD install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Failed to install dependencies"
        echo "Trying basic dependencies as fallback..."
        $PIP_CMD install -r requirements-basic.txt
        
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install basic dependencies"
            echo "Please check your internet connection and try again"
            exit 1
        fi
    fi
fi

# Install system dependencies based on OS
echo
echo "Checking system dependencies..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux - checking for required packages..."
    if command -v apt &> /dev/null; then
        echo "Installing system dependencies with apt..."
        sudo apt update
        sudo apt install -y ffmpeg libsndfile1-dev
    elif command -v yum &> /dev/null; then
        echo "Installing system dependencies with yum..."
        sudo yum install -y ffmpeg libsndfile-devel
    elif command -v pacman &> /dev/null; then
        echo "Installing system dependencies with pacman..."
        sudo pacman -S --noconfirm ffmpeg libsndfile
    else
        echo "Please install ffmpeg and libsndfile manually"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS - checking for Homebrew..."
    if command -v brew &> /dev/null; then
        echo "Installing system dependencies with Homebrew..."
        brew install ffmpeg libsndfile
    else
        echo "Please install Homebrew and run: brew install ffmpeg libsndfile"
    fi
fi

echo
echo "============================================"
echo "Installation completed successfully!"
echo "============================================"
echo
echo "To get started:"
echo "1. Place your EPUB files in the 'input' folder"

# Check Python version again for instructions
PYTHON_VERSION_CHECK=$($PYTHON_CMD -c "import sys; print('high' if sys.version_info >= (3, 12) else 'ok')")
if [ "$PYTHON_VERSION_CHECK" = "high" ]; then
    echo "2. Try demo first: $PYTHON_CMD demo.py -i input/your_book.epub"
    echo "3. For full conversion, use Python 3.8-3.11 or try: $PYTHON_CMD main.py -i input/your_book.epub"
else
    echo "2. Run: $PYTHON_CMD main.py -i input/your_book.epub"
fi
echo "4. Check the 'output' folder for your audiobook"
echo
echo "For help: $PYTHON_CMD main.py --help"
echo "For examples: $PYTHON_CMD examples.py"
echo
echo "Optional: Install GPU support for faster processing"
echo "  $PIP_CMD install torch torchaudio --index-url https://download.pytorch.org/whl/cu118"
echo

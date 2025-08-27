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
$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
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
echo "2. Run: $PYTHON_CMD main.py -i input/your_book.epub"
echo "3. Check the 'output' folder for your audiobook"
echo
echo "For help: $PYTHON_CMD main.py --help"
echo "For examples: $PYTHON_CMD examples.py"
echo
echo "Optional: Install GPU support for faster processing"
echo "  $PIP_CMD install torch torchaudio --index-url https://download.pytorch.org/whl/cu118"
echo

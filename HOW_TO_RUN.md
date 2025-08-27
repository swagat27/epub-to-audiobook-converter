# How to Run the EPUB to Audiobook Converter

## 🎯 Quickest Way to Get Started

```bash
# 1. Check if you're ready to go
python check_setup.py

# 2. Use the interactive helper (recommended for beginners)
python run.py

# 3. Or jump straight to conversion
python main.py -i "path/to/your/book.epub"
```

## Quick Start Guide

### 1. Check Your Python Version
```bash
python --version
```
**Important**: This application works best with Python 3.8-3.11. Python 3.12+ has compatibility issues with the TTS library.

### 2. Install Dependencies
```bash
# Basic installation
pip install -r requirements-basic.txt

# Full installation (if Python 3.8-3.11)
pip install -r requirements.txt
```

### 3. Install System Dependencies
- **Windows**: Download FFmpeg from https://ffmpeg.org and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg libsndfile1-dev`

### 4. Run the Application

#### Option A: Demo Version (No TTS, just text extraction)
```bash
python demo.py -i "path/to/your/book.epub"
```

#### Option B: Full Conversion (Requires TTS dependencies)
```bash
python main.py -i "path/to/your/book.epub"
```

#### Option C: Examples and Testing
```bash
python examples.py
```

## Common Commands

```bash
# Basic conversion
python main.py -i "book.epub"

# Specify output directory
python main.py -i "book.epub" -o "my_audiobooks"

# Use MP3 format instead of M4B
python main.py -i "book.epub" -f mp3

# Enable GPU acceleration
python main.py -i "book.epub" --gpu

# Adjust speech speed
python main.py -i "book.epub" --speed 1.2

# Use Spanish voice
python main.py -i "book.epub" -v es

# Debug mode
python main.py -i "book.epub" --log-level DEBUG

# Get help
python main.py --help
```

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements-basic.txt
```

### TTS Installation Issues (Python 3.12+)
Try the demo version instead:
```bash
python demo.py -i "book.epub"
```

### FFmpeg Not Found
Install FFmpeg for your operating system (see step 3 above).

### GPU Issues
Run without GPU acceleration:
```bash
python main.py -i "book.epub" --no-gpu
```

## File Structure After Installation

```
epub-to-audiobook-converter/
├── main.py              # Main application
├── demo.py              # Demo version (no TTS)
├── examples.py          # Example usage
├── input/               # Place your EPUB files here
├── output/              # Generated audiobooks appear here
├── requirements.txt     # Python dependencies
├── requirements-basic.txt # Basic dependencies only
└── logs/               # Application logs
```

## Output

- **M4B files**: Audiobook format with chapter markers
- **MP3 files**: Standard audio format
- **Logs**: Check `logs/` directory for detailed execution logs
- **Metadata**: Automatically extracted from EPUB and added to audiobook

---

For more detailed information, see the full README.md file.
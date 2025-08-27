# EPUB to Audiobook Converter - Installation Guide

## Quick Setup for Python 3.12

Since you're using Python 3.12, some dependencies in the original requirements.txt may not be compatible. Follow these steps:

### 1. Check Dependencies
First, check what's available:
```bash
python3 main.py check
```

### 2. Install Basic Dependencies
Try installing the basic dependencies first:
```bash
pip install click colorama ebooklib beautifulsoup4 lxml pydub mutagen numpy tqdm
```

### 3. Install Audio Dependencies
For audio processing:
```bash
pip install librosa soundfile
```

### 4. Install PyTorch (for TTS)
For TTS functionality, install PyTorch compatible with Python 3.12:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
# OR for CUDA support:
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 5. Install TTS (when available)
The TTS package may need to be installed from source or a newer version:
```bash
# Check if TTS is available for Python 3.12:
pip install TTS
# If that fails, you may need to wait for TTS package update or use Python 3.11
```

### 6. Test Installation
Run the examples to see what's working:
```bash
python3 examples.py
```

### 7. Check Full Functionality
Try the dependency check again:
```bash
python3 main.py check
```

## Troubleshooting

### If TTS is not available
- The application will still run basic text processing and configuration examples
- Consider using Python 3.11 environment for full TTS support
- Or wait for TTS package to support Python 3.12

### Alternative: Use Python 3.11
If you need full TTS functionality immediately:
```bash
# Create a Python 3.11 environment
conda create -n epub-converter python=3.11
conda activate epub-converter
pip install -r requirements.txt
```
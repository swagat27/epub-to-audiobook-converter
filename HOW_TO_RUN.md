# 🚀 How to Run EPUB to Audiobook Converter

## 📋 Prerequisites Check

### 1. Verify Your Setup
```bash
# Check Python version
python --version
# Should show Python 3.x.x

# Check if you're in the right directory
pwd
# Should show: ...epub-to-audiobook-converter

# Test basic imports
python -c "from src.config_manager import ConfigManager; print('✅ Basic setup OK')"
```

## 🎧 Running the Application

### Basic Command Structure
```bash
python main.py --input <epub-file> [options]
```

### 📖 Required Arguments
- `--input` or `-i`: Path to your EPUB file

### ⚙️ Optional Arguments
- `--output` or `-o`: Output directory (default: ./output)
- `--voice` or `-v`: Voice/language (default: en)
- `--speaker` or `-s`: Speaker style (default: default)
- `--speed`: Speech speed multiplier (default: 1.0)
- `--pitch`: Pitch multiplier (default: 1.0)
- `--format` or `-f`: Output format [mp3, m4b] (default: m4b)
- `--gpu`: Enable GPU acceleration
- `--config` or `-c`: Path to configuration file
- `--log-level`: Logging level [DEBUG, INFO, WARNING, ERROR]
- `--chapter-pause`: Pause between chapters in seconds (default: 2.0)

## 🎯 Step-by-Step Examples

### Example 1: Basic Conversion
```bash
# Convert an EPUB file with default settings
python main.py --input "my-book.epub"
```

### Example 2: Custom Output Directory
```bash
# Specify where to save the audiobook
python main.py --input "my-book.epub" --output "C:\My Audiobooks"
```

### Example 3: Adjust Speech Settings
```bash
# Slower speech, lower pitch
python main.py --input "my-book.epub" --speed 0.8 --pitch 0.9
```

### Example 4: Different Output Format
```bash
# Create MP3 instead of M4B
python main.py --input "my-book.epub" --format mp3
```

### Example 5: Verbose Logging
```bash
# See detailed progress information
python main.py --input "my-book.epub" --log-level DEBUG
```

## 📁 File Structure for Running

```
your-project/
├── main.py              ← Main script to run
├── config/
│   └── default_config.json
├── src/                 ← Source modules
├── input/               ← Place your EPUB files here
├── output/              ← Generated audiobooks appear here
└── logs/                ← Log files
```

## 🧪 Testing the Application

### 1. Test with Help Command
```bash
python main.py --help
```

### 2. Test Dependencies
```bash
python test_imports.py
```

### 3. Test with Sample File
```bash
# If you have a sample EPUB file
python main.py --input "input/sample-book.epub" --log-level INFO
```

## ⚠️ Current Limitations (Python 3.13)

Since you're using Python 3.13, be aware that:
- ✅ Basic functionality works
- ⚠️ TTS quality may be limited (using fallback engine)
- 🔧 For best results, consider Python 3.11/3.12

## 🛠️ Troubleshooting

### If you get "No module named..." errors:
```bash
# Install missing dependencies
pip install ebooklib beautifulsoup4 pydub click colorama tqdm mutagen
pip install pyttsx3  # Fallback TTS engine
```

### If FFmpeg warnings appear:
- Download FFmpeg from https://ffmpeg.org/
- Add to your system PATH
- Restart terminal

### If the application hangs:
- Check your EPUB file is valid
- Try with `--log-level DEBUG` to see what's happening
- Ensure sufficient disk space

## 📊 Expected Output

When running successfully, you'll see:
```
📚 EPUB to Audiobook Converter
Converting: your-book.epub
Output: ./output

✓ Found X chapters
Converting chapters ████████████ 100%
✓ Generated X audio files
🎉 Audiobook created successfully!
Output file: ./output/your-book.m4b
File size: XX.XX MB
```

## 🚨 Quick Start Checklist

1. ✅ Navigate to project directory
2. ✅ Have an EPUB file ready
3. ✅ Run: `python main.py --input "your-book.epub"`
4. ✅ Wait for conversion to complete
5. ✅ Find your audiobook in the `output/` folder

## 💡 Pro Tips

- Start with a small EPUB file for testing
- Use `--log-level DEBUG` if something goes wrong
- Check the `logs/` folder for detailed error information
- The first run may take longer as it downloads TTS models
- GPU acceleration (`--gpu`) can speed up processing if you have NVIDIA GPU

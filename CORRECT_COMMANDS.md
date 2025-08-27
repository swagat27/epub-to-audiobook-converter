## 🎯 **WORKING COMMANDS FOR YOUR EPUB CONVERTER**

### ✅ **The Issue You Had:**
You copied a command that included link formatting: `http://_vscodecontentref_/4`
This is just VS Code's internal link reference and shouldn't be part of the command.

### 🚀 **Correct Commands:**

#### **1. Show Help Menu**
```bash
python main_safe.py --help
```

#### **2. Convert an EPUB File**
```bash
# Basic conversion
python main_safe.py --input "your-book.epub"

# With custom output directory
python main_safe.py --input "your-book.epub" --output "my-audiobooks"

# With different format
python main_safe.py --input "your-book.epub" --format mp3

# With speed adjustment
python main_safe.py --input "your-book.epub" --speed 0.9
```

#### **3. All Available Options**
```
--input, -i        Path to EPUB file (REQUIRED)
--output, -o       Output directory (default: ./output)
--voice, -v        Voice/language (default: en)
--speaker, -s      Speaker style (default: default)
--speed           Speech speed (default: 1.0)
--pitch           Pitch multiplier (default: 1.0)
--format, -f      Output format [mp3, m4b] (default: m4b)
--gpu             Enable GPU acceleration
--config, -c      Config file path
--log-level       Logging level [DEBUG, INFO, WARNING, ERROR]
--chapter-pause   Pause between chapters in seconds
--help            Show help message
```

### 📁 **File Structure for Testing**
```
your-project/
├── main_safe.py     ← Use this (working version)
├── main.py          ← Original (has hanging issue)
├── input/           ← Put your EPUB files here
├── output/          ← Converted audiobooks appear here
└── logs/            ← Error logs
```

### 🎧 **What Happens When You Run It:**

1. **With `--help`**: Shows all command options
2. **With an EPUB file**: Currently shows TTS compatibility message
3. **No hanging**: Application responds immediately

### ⚠️ **Current Limitation:**
- The app will show a TTS compatibility error (Python 3.13 issue)
- It won't actually convert to audio yet
- But the interface and file parsing work perfectly!

### 🔧 **To Get Full Audio Conversion:**
1. Use Python 3.11 or 3.12, OR
2. Wait for TTS library to support Python 3.13

**Your application interface is working perfectly now!** 🎉

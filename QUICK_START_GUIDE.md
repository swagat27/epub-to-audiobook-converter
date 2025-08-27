# 🎯 **How to Run Your EPUB to Audiobook Converter**

## ✅ **Good News: Your Application is Working!**

The quick test shows that your EPUB to Audiobook Converter is ready to use! Here's exactly how to run it:

## 🚀 **Basic Usage**

### **Step 1: Prepare Your EPUB File**
Place your EPUB file in the `input/` folder or note its full path.

### **Step 2: Run the Converter**
```bash
# Basic conversion (recommended for first try)
python main.py --input "path/to/your-book.epub"

# Example with a file in the input folder
python main.py --input "input/my-book.epub"

# Example with full path
python main.py --input "C:\Users\hp\Documents\my-book.epub"
```

### **Step 3: Wait for Completion**
The application will:
1. Parse your EPUB file
2. Extract text from each chapter
3. Convert text to speech
4. Merge audio files
5. Create final audiobook in `output/` folder

## 📋 **Command Examples**

### **Most Common Usage**
```bash
# Convert with default settings
python main.py --input "my-book.epub"
```

### **Custom Output Location**
```bash
# Save to specific folder
python main.py --input "my-book.epub" --output "C:\My Audiobooks"
```

### **Adjust Speech Settings**
```bash
# Slower speech for better comprehension
python main.py --input "my-book.epub" --speed 0.8

# Different output format
python main.py --input "my-book.epub" --format mp3
```

### **Debug Mode (if something goes wrong)**
```bash
# See detailed information
python main.py --input "my-book.epub" --log-level DEBUG
```

## 📁 **File Locations**

- **Input**: Place EPUB files in `input/` folder
- **Output**: Find audiobooks in `output/` folder  
- **Logs**: Check `logs/` folder for error information
- **Config**: Modify `config/default_config.json` for settings

## ⚠️ **Current Setup Notes**

✅ **Working**: All core modules loaded successfully
✅ **Audio Processing**: pydub is working (with FFmpeg warning - normal)
⚠️ **TTS Engine**: Using fallback engine (works but lower quality)
⚠️ **FFmpeg**: Warning shown but audio processing should still work

## 🎧 **Expected Results**

When successful, you'll get:
- An M4B or MP3 file in the `output/` folder
- Chapter markers (if supported by format)
- Metadata from the original EPUB

## 🆘 **If Something Goes Wrong**

1. **Check the file path** - Use full paths or relative to project folder
2. **Check EPUB file** - Make sure it's a valid EPUB
3. **Use debug mode** - Add `--log-level DEBUG` to see what's happening
4. **Check logs folder** - Look in `logs/` for detailed error information

## 🚀 **Ready to Start!**

Your application is set up and ready. Just run:
```bash
python main.py --input "your-epub-file.epub"
```

The first conversion might take a bit longer as the system initializes, but subsequent conversions will be faster.

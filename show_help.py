#!/usr/bin/env python3
"""
Help and documentation display for the EPUB to Audiobook Converter.
Shows what the help commands would display if dependencies were available.
"""

def show_main_help():
    """Show the help for main.py application."""
    print("=" * 80)
    print("📚 main.py --help")
    print("=" * 80)
    print("""Usage: main.py [OPTIONS]

  Convert EPUB eBooks to audiobooks using advanced text-to-speech technology.

  This application parses EPUB files chapter by chapter, converts text to
  speech using high-quality TTS engines, and merges the audio into a single
  audiobook file with proper metadata and chapter markers.

Options:
  -i, --input PATH                Path to the input EPUB file  [required]
  -o, --output PATH               Output directory for the audiobook
                                  (default: ./output)
  -v, --voice TEXT                Voice/language for TTS (default: en)
  -s, --speaker TEXT              Speaker voice style (default: default)
  --speed FLOAT                   Speech speed multiplier (default: 1.0)
  --pitch FLOAT                   Pitch multiplier (default: 1.0)
  -f, --format [mp3|m4b]          Output audio format (default: m4b)
  --gpu                           Enable GPU acceleration for TTS processing
  -c, --config PATH               Path to configuration file
  --log-level [DEBUG|INFO|WARNING|ERROR]
                                  Logging level (default: INFO)
  --chapter-pause FLOAT           Pause duration between chapters in seconds
                                  (default: 2.0)
  --help                          Show this message and exit.
""")

def show_demo_help():
    """Show the help for demo.py application."""
    print("=" * 80)
    print("📖 demo.py --help")
    print("=" * 80)
    print("""Usage: demo.py [OPTIONS]

  Demo: Parse EPUB files and extract clean text (without TTS conversion).

  This demo version shows the text extraction and cleaning capabilities
  without requiring the heavy TTS dependencies.

Options:
  -i, --input PATH                Path to the input EPUB file  [required]
  -o, --output PATH               Output directory for the text files
                                  (default: ./output)
  --log-level [DEBUG|INFO|WARNING|ERROR]
                                  Logging level (default: INFO)
  --help                          Show this message and exit.
""")

def show_installation_guide():
    """Show installation instructions."""
    print("=" * 80)
    print("🛠️ Installation Guide")
    print("=" * 80)
    print("""
PREREQUISITES:
  • Python 3.8 or higher
  • pip package manager
  • Optional: CUDA-compatible GPU for acceleration

INSTALLATION METHODS:

1. AUTOMATIC INSTALLATION (Recommended):
   
   Windows:
     install.bat
   
   Linux/macOS:
     ./install.sh

2. MANUAL INSTALLATION:
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # For GPU acceleration (optional)
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

3. SYSTEM DEPENDENCIES:
   
   Windows:
     • Download FFmpeg from https://ffmpeg.org/download.html
     • Add FFmpeg to your system PATH
   
   macOS:
     brew install ffmpeg
   
   Ubuntu/Debian:
     sudo apt update
     sudo apt install ffmpeg libsndfile1-dev
   
   RHEL/CentOS/Fedora:
     sudo yum install ffmpeg libsndfile-devel

VERIFICATION:
   # Test basic functionality
   python demo.py --help
   
   # Test full application (requires all dependencies)
   python main.py --help
""")

def show_usage_scenarios():
    """Show different usage scenarios."""
    print("=" * 80)
    print("📖 Usage Scenarios")
    print("=" * 80)
    print("""
SCENARIO 1: Basic Conversion
  Goal: Convert an EPUB to audiobook with default settings
  
  Steps:
    1. Place your EPUB file in the 'input' directory
    2. Run: python main.py -i input/your_book.epub
    3. Wait for processing to complete
    4. Find your audiobook in the 'output' directory
  
  Example:
    python main.py -i input/harry_potter.epub

SCENARIO 2: High-Quality Professional Conversion
  Goal: Create high-quality audiobook with custom settings
  
  Command:
    python main.py \\
      --input "input/my_book.epub" \\
      --output "./audiobooks" \\
      --voice en \\
      --speed 1.1 \\
      --pitch 0.95 \\
      --format m4b \\
      --gpu \\
      --log-level INFO

SCENARIO 3: Batch Processing
  Goal: Convert multiple books automatically
  
  Linux/macOS:
    for book in input/*.epub; do
        python main.py -i "$book" -o "./output" --gpu
    done
  
  Windows (PowerShell):
    Get-ChildItem input/*.epub | ForEach-Object {
        python main.py -i $_.FullName -o "./output" --gpu
    }

SCENARIO 4: Testing and Development
  Goal: Test the application without full TTS processing
  
  Commands:
    # Parse EPUB and show structure
    python demo.py -i input/test_book.epub
    
    # Run examples and see programmatic usage
    python examples.py

SCENARIO 5: Custom Configuration
  Goal: Use a configuration file for repeated conversions
  
  Steps:
    1. Create config file: config/my_settings.json
    2. Run: python main.py -i input/book.epub -c config/my_settings.json
  
  Example config:
    {
      "tts_settings": {
        "voice": "en",
        "speed": 1.2,
        "pitch": 0.9,
        "gpu_acceleration": true
      },
      "audio_settings": {
        "output_format": "m4b",
        "chapter_pause": 3.0
      }
    }
""")

def show_troubleshooting():
    """Show troubleshooting information."""
    print("=" * 80)
    print("🔧 Troubleshooting")
    print("=" * 80)
    print("""
COMMON ISSUES AND SOLUTIONS:

1. ImportError: No module named 'ebooklib'
   Solution: pip install -r requirements.txt

2. CUDA not detected / GPU acceleration not working
   Solution: Install CUDA-compatible PyTorch
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

3. Audio quality issues
   Solutions:
   • Try different TTS models
   • Adjust speed/pitch settings
   • Use higher quality audio settings

4. Memory errors during processing
   Solutions:
   • Reduce batch size in configuration
   • Disable GPU acceleration
   • Process smaller books first

5. File format not supported
   Solution: Ensure input file is a valid EPUB format

6. Slow processing speed
   Solutions:
   • Enable GPU acceleration with --gpu
   • Use faster TTS models
   • Process on a machine with more RAM/CPU

DEBUG MODE:
   Enable detailed logging for troubleshooting:
   python main.py -i book.epub --log-level DEBUG

LOG FILES:
   Check logs directory for detailed execution logs:
   • logs/epub_to_audiobook.log - Main application log
   • Console output for real-time progress

SUPPORT:
   • Check README.md for detailed documentation
   • Review examples.py for usage patterns
   • Test with demo.py to isolate issues
""")

def main():
    """Show all help and documentation."""
    print("🎵 EPUB to Audiobook Converter - Complete Documentation 🎵")
    print()
    
    show_main_help()
    print()
    
    show_demo_help()
    print()
    
    show_installation_guide()
    print()
    
    show_usage_scenarios()
    print()
    
    show_troubleshooting()
    
    print("=" * 80)
    print("✅ Documentation Complete")
    print("=" * 80)
    print("Ready to convert your EPUB files to audiobooks! 🎧")

if __name__ == "__main__":
    main()
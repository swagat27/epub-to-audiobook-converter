#!/usr/bin/env python3
"""
Validation script to check if the EPUB to Audiobook Converter is ready to run.
This script checks dependencies and provides guidance on how to run the application.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    
    if version >= (3, 12):
        print("⚠️  WARNING: Python 3.12+ detected. TTS library may not be compatible.")
        print("   Recommendation: Use Python 3.8-3.11 for full functionality")
        return "warning"
    elif version >= (3, 8):
        print("✓ Python version is compatible with all features")
        return "ok"
    else:
        print("❌ ERROR: Python 3.8+ required")
        return "error"

def check_dependencies():
    """Check if required dependencies are installed."""
    basic_deps = ['click', 'colorama']
    full_deps = ['ebooklib', 'beautifulsoup4', 'TTS']
    
    missing_basic = []
    missing_full = []
    
    print("\nChecking basic dependencies:")
    for dep in basic_deps:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing_basic.append(dep)
    
    print("\nChecking full dependencies:")
    for dep in full_deps:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing_full.append(dep)
    
    return missing_basic, missing_full

def check_system_deps():
    """Check system dependencies."""
    print("\nChecking system dependencies:")
    
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ FFmpeg")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg (required for audio processing)")
        return False
    
    return True

def check_project_structure():
    """Check if project structure is correct."""
    print("\nChecking project structure:")
    
    required_files = [
        'main.py',
        'demo.py',
        'requirements.txt',
        'requirements-basic.txt',
        'src/epub_parser.py',
        'src/text_processor.py',
        'src/config_manager.py'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return missing_files

def provide_recommendations(python_status, missing_basic, missing_full, missing_files, ffmpeg_ok):
    """Provide recommendations based on the checks."""
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    if missing_files:
        print("❌ Project structure incomplete. Please ensure you have the full repository.")
        return
    
    if python_status == "error":
        print("❌ Please upgrade to Python 3.8 or higher")
        return
    
    if missing_basic:
        print("📦 Install basic dependencies:")
        print("   pip install -r requirements-basic.txt")
        print("   OR: pip install click colorama")
    
    if python_status == "warning":
        print("\n⚠️  Python 3.12+ detected:")
        print("   • Try demo version first: python demo.py --help")
        print("   • For full TTS features, consider Python 3.8-3.11")
        print("   • Or try manual TTS install: pip install TTS --no-deps")
    elif missing_full:
        print("\n📦 Install full dependencies:")
        print("   pip install -r requirements.txt")
    
    if not ffmpeg_ok:
        print("\n🔧 Install FFmpeg:")
        print("   • Windows: Download from https://ffmpeg.org and add to PATH")
        print("   • macOS: brew install ffmpeg")
        print("   • Linux: sudo apt install ffmpeg")
    
    print("\n🚀 HOW TO RUN:")
    if missing_basic or (python_status == "warning" and missing_full):
        print("   1. Install dependencies (see above)")
        print("   2. Try demo: python demo.py --help")
    else:
        print("   1. Place EPUB files in input/ directory")
        if python_status == "warning":
            print("   2. Try demo: python demo.py -i input/book.epub")
            print("   3. Or try main: python main.py -i input/book.epub")
        else:
            print("   2. Run: python main.py -i input/book.epub")
        print("   3. Check output/ directory for results")
    
    print("\n📚 For detailed instructions, see:")
    print("   • README.md")
    print("   • HOW_TO_RUN.md")

def main():
    """Main validation function."""
    print("EPUB to Audiobook Converter - System Check")
    print("="*60)
    
    # Run all checks
    python_status = check_python_version()
    missing_basic, missing_full = check_dependencies()
    ffmpeg_ok = check_system_deps()
    missing_files = check_project_structure()
    
    # Provide recommendations
    provide_recommendations(python_status, missing_basic, missing_full, missing_files, ffmpeg_ok)

if __name__ == "__main__":
    main()
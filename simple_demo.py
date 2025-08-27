#!/usr/bin/env python3
"""
Simple demonstration of the EPUB to Audiobook Converter
This script shows how to use the application with minimal dependencies.
"""

import os
import sys
from pathlib import Path

def show_help():
    """Display help information about the application."""
    print("=" * 60)
    print("📚 EPUB to Audiobook Converter - Help")
    print("=" * 60)
    print()
    print("This application converts EPUB eBooks to audiobooks using TTS.")
    print()
    print("MAIN APPLICATION (main.py):")
    print("  python main.py -i input.epub -o output/")
    print()
    print("DEMO VERSION (demo.py):")
    print("  python demo.py -i input.epub -o output/")
    print()
    print("EXAMPLES:")
    print("  python examples.py")
    print()
    print("REQUIRED ARGUMENTS:")
    print("  -i, --input    Path to input EPUB file")
    print()
    print("OPTIONAL ARGUMENTS:")
    print("  -o, --output   Output directory (default: ./output)")
    print("  -v, --voice    Voice/language for TTS (default: en)")
    print("  -s, --speaker  Speaker voice style (default: default)")
    print("  --speed        Speech speed multiplier (default: 1.0)")
    print("  --pitch        Pitch multiplier (default: 1.0)")
    print("  -f, --format   Output format: mp3 or m4b (default: m4b)")
    print("  --gpu          Enable GPU acceleration")
    print("  --log-level    Logging level: DEBUG, INFO, WARNING, ERROR")
    print()
    print("EXAMPLES:")
    print("  # Basic conversion")
    print("  python main.py -i book.epub")
    print()
    print("  # Custom settings")
    print("  python main.py -i book.epub -v en --speed 1.2 --gpu")
    print()
    print("  # Demo mode (no TTS, text extraction only)")
    print("  python demo.py -i book.epub")
    print()
    
def check_dependencies():
    """Check which dependencies are available."""
    print("=" * 60)
    print("📦 Dependency Check")
    print("=" * 60)
    
    required_packages = [
        'ebooklib',
        'beautifulsoup4', 
        'lxml',
        'click',
        'colorama',
        'TTS',
        'torch',
        'pydub',
        'mutagen'
    ]
    
    available = []
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            available.append(package)
            print(f"✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"✗ {package}")
    
    print()
    print(f"Available: {len(available)}/{len(required_packages)}")
    print(f"Missing: {len(missing)}")
    
    if missing:
        print()
        print("To install missing packages:")
        print(f"pip install {' '.join(missing)}")
        print()
        print("Or install all at once:")
        print("pip install -r requirements.txt")
    
    return len(missing) == 0

def create_sample_epub():
    """Create a simple sample EPUB file for testing."""
    sample_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Sample Book</title>
</head>
<body>
    <h1>Chapter 1: Introduction</h1>
    <p>This is a sample chapter for testing the EPUB to audiobook converter.</p>
    <p>It contains multiple paragraphs to demonstrate text processing.</p>
    
    <h1>Chapter 2: Main Content</h1>
    <p>This is the second chapter with more content.</p>
    <p>The converter will process each chapter separately.</p>
</body>
</html>"""
    
    sample_file = Path("input/sample.txt")
    sample_file.parent.mkdir(exist_ok=True)
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"📄 Created sample text file: {sample_file}")
    print("Note: This is a text file, not an EPUB. For real testing, provide an actual EPUB file.")
    
def show_file_structure():
    """Show the project file structure."""
    print("=" * 60)
    print("📁 Project Structure")
    print("=" * 60)
    
    important_files = [
        "main.py",
        "demo.py", 
        "examples.py",
        "requirements.txt",
        "README.md",
        "src/",
        "input/",
        "output/",
        "config/"
    ]
    
    for file_path in important_files:
        path = Path(file_path)
        if path.exists():
            if path.is_dir():
                print(f"📁 {file_path}")
                # Show some contents of directories
                try:
                    for item in sorted(path.iterdir())[:5]:
                        print(f"   📄 {item.name}")
                    if len(list(path.iterdir())) > 5:
                        print(f"   ... and {len(list(path.iterdir())) - 5} more files")
                except:
                    pass
            else:
                size = path.stat().st_size
                print(f"📄 {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} (missing)")
    print()

def demonstrate_usage():
    """Show how to use the application."""
    print("=" * 60)
    print("🚀 Usage Demonstration")
    print("=" * 60)
    print()
    
    print("1. BASIC USAGE:")
    print("   Place your EPUB file in the 'input/' directory")
    print("   Run: python main.py -i input/your_book.epub")
    print()
    
    print("2. DEMO MODE (recommended if dependencies are missing):")
    print("   Run: python demo.py -i input/your_book.epub")
    print("   This will extract and process text without TTS conversion")
    print()
    
    print("3. VIEW EXAMPLES:")
    print("   Run: python examples.py")
    print("   This shows programmatic usage examples")
    print()
    
    print("4. GET HELP:")
    print("   Run: python main.py --help")
    print("   Run: python demo.py --help")
    print()

def main():
    """Main demonstration function."""
    print()
    print("🎵 EPUB to Audiobook Converter 🎵")
    print()
    
    # Show basic information
    show_help()
    print()
    
    # Check dependencies
    all_deps_available = check_dependencies()
    print()
    
    # Show file structure
    show_file_structure()
    
    # Create sample file if none exists
    if not any(Path("input").glob("*.epub")):
        create_sample_epub()
        print()
    
    # Show usage instructions
    demonstrate_usage()
    
    # Provide next steps
    print("=" * 60)
    print("🎯 Next Steps")
    print("=" * 60)
    
    if all_deps_available:
        print("✅ All dependencies are available!")
        print("You can run the full application:")
        print("  python main.py -i input/your_book.epub")
    else:
        print("⚠️  Some dependencies are missing.")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Or try demo mode: python demo.py -i input/your_book.epub")
    
    print()
    print("📚 Place your EPUB files in the 'input/' directory")
    print("🎧 Output audiobooks will be saved to 'output/' directory")
    print()

if __name__ == "__main__":
    main()
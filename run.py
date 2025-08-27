#!/usr/bin/env python3
"""
Simple wrapper script to help users run the EPUB to Audiobook Converter.
This script provides guidance and tries to run the appropriate version based on available dependencies.
"""

import sys
import os
from pathlib import Path

def print_header():
    """Print a friendly header."""
    print("=" * 60)
    print("📚 EPUB to Audiobook Converter")
    print("=" * 60)
    print()

def check_and_guide():
    """Check system and provide guidance."""
    # Check Python version
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro} detected")
    
    # Check basic dependencies
    deps_available = {
        'ebooklib': False,
        'click': False,
        'TTS': False
    }
    
    for dep in deps_available:
        try:
            __import__(dep)
            deps_available[dep] = True
        except ImportError:
            pass
    
    print()
    if deps_available['ebooklib'] and deps_available['click']:
        print("✓ Basic dependencies available")
        if deps_available['TTS']:
            print("✓ TTS engine available - full functionality ready!")
            return 'full'
        else:
            print("⚠️  TTS engine not available - demo mode only")
            return 'demo'
    else:
        print("❌ Missing basic dependencies")
        return 'missing'

def show_installation_help():
    """Show installation help."""
    print("📦 INSTALLATION NEEDED")
    print("-" * 30)
    print()
    print("To install dependencies, run one of these:")
    print()
    print("Option 1 - Use install script:")
    if os.name == 'nt':  # Windows
        print("  install.bat")
    else:  # Unix/Linux/macOS
        print("  ./install.sh")
    print()
    print("Option 2 - Manual installation:")
    print("  pip install -r requirements-basic.txt")
    print("  pip install -r requirements.txt  # for full TTS features")
    print()
    print("Option 3 - Check what's wrong:")
    print("  python check_setup.py")
    print()

def show_usage_help(mode):
    """Show usage help based on available mode."""
    print("🚀 HOW TO USE")
    print("-" * 30)
    print()
    print("1. Place your EPUB files in the 'input/' directory")
    print("2. Run the appropriate command:")
    print()
    
    if mode == 'full':
        print("   Full conversion (with audio):")
        print("   python main.py -i input/your_book.epub")
        print()
        print("   Quick demo (text only):")
        print("   python demo.py -i input/your_book.epub")
    elif mode == 'demo':
        print("   Demo mode (text extraction only):")
        print("   python demo.py -i input/your_book.epub")
        print()
        print("   For full audio conversion, install TTS:")
        print("   pip install TTS")
    
    print()
    print("3. Check the 'output/' directory for results")
    print()
    print("📋 More options:")
    print("   python main.py --help     # See all options")
    print("   python examples.py        # View examples")
    print("   python check_setup.py     # Check system status")
    print()

def try_run_interactive():
    """Try to run in interactive mode."""
    print("🎯 QUICK START")
    print("-" * 30)
    
    # Check if input directory exists and has EPUB files
    input_dir = Path('input')
    if not input_dir.exists():
        print("Creating input/ directory...")
        input_dir.mkdir(exist_ok=True)
    
    epub_files = list(input_dir.glob('*.epub'))
    if not epub_files:
        print("No EPUB files found in input/ directory.")
        print("Please place your .epub files there and try again.")
        return
    
    print(f"Found {len(epub_files)} EPUB file(s):")
    for i, epub in enumerate(epub_files, 1):
        print(f"  {i}. {epub.name}")
    
    if len(epub_files) == 1:
        selected_file = epub_files[0]
    else:
        try:
            choice = input(f"\nSelect file (1-{len(epub_files)}): ").strip()
            selected_file = epub_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return
    
    print(f"\nSelected: {selected_file.name}")
    
    # Determine which script to run
    mode = check_and_guide()
    if mode == 'missing':
        print("Cannot run conversion - missing dependencies.")
        return
    
    script = 'demo.py' if mode == 'demo' else 'main.py'
    command = f'python {script} -i "{selected_file}"'
    
    print(f"\nRunning: {command}")
    print("=" * 60)
    
    # Execute the command
    os.system(command)

def main():
    """Main function."""
    print_header()
    
    # Check if any command line arguments were provided
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("This script helps you run the EPUB to Audiobook Converter.")
            print()
            print("Usage:")
            print("  python run.py          # Interactive mode")
            print("  python run.py --help   # Show this help")
            print("  python run.py --check  # Check system status")
            print()
            return
        elif sys.argv[1] == '--check':
            os.system('python check_setup.py')
            return
    
    # Main logic
    mode = check_and_guide()
    print()
    
    if mode == 'missing':
        show_installation_help()
    else:
        show_usage_help(mode)
        
        # Ask if user wants to try interactive mode
        try:
            if input("Try interactive mode? (y/n): ").lower().startswith('y'):
                print()
                try_run_interactive()
        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Debug version of main script to identify hanging issues
"""

print("🔍 Debug: Starting imports...")

try:
    print("1. Importing standard libraries...")
    import os
    import sys
    import logging
    from pathlib import Path
    print("✅ Standard libraries OK")
    
    print("2. Importing click...")
    import click
    print("✅ Click OK")
    
    print("3. Importing colorama...")
    from colorama import init, Fore, Style
    init()
    print("✅ Colorama OK")
    
    print("4. Importing config manager...")
    from src.config_manager import ConfigManager
    print("✅ Config Manager OK")
    
    print("5. Importing logger...")
    from src.logger import setup_logger
    print("✅ Logger OK")
    
    print("6. Importing EPUB parser...")
    from src.epub_parser import EPUBParser
    print("✅ EPUB Parser OK")
    
    print("7. Importing text processor...")
    from src.text_processor import TextProcessor
    print("✅ Text Processor OK")
    
    print("8. Importing audio processor...")
    from src.audio_processor import AudioProcessor
    print("✅ Audio Processor OK")
    
    print("9. Testing TTS engine import...")
    from src.tts_engine import TTSEngine
    print("✅ TTS Engine OK")
    
    print("\n🎉 All imports successful!")
    
    # Test click command creation
    print("\n10. Testing click command...")
    
    @click.command()
    @click.option('--test', default='hello', help='Test option')
    def test_command(test):
        """Test command to verify click works"""
        click.echo(f"Test successful: {test}")
    
    print("✅ Click command creation OK")
    print("\n🎉 Main script should work now!")
    
except Exception as e:
    print(f"❌ Error during import: {e}")
    import traceback
    traceback.print_exc()

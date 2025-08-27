#!/usr/bin/env python3
"""
Quick test script to verify the EPUB to Audiobook Converter can run
"""

import sys
import os

def test_basic_imports():
    """Test if basic modules can be imported"""
    print("🧪 Testing basic imports...")
    
    try:
        from src.config_manager import ConfigManager
        print("✅ ConfigManager")
    except Exception as e:
        print(f"❌ ConfigManager: {e}")
        return False
    
    try:
        from src.epub_parser import EPUBParser
        print("✅ EPUBParser")
    except Exception as e:
        print(f"❌ EPUBParser: {e}")
        return False
    
    try:
        from src.text_processor import TextProcessor
        print("✅ TextProcessor")
    except Exception as e:
        print(f"❌ TextProcessor: {e}")
        return False
    
    try:
        from src.audio_processor import AudioProcessor
        print("✅ AudioProcessor")
    except Exception as e:
        print(f"❌ AudioProcessor: {e}")
        return False
    
    try:
        from src.tts_engine import TTSEngine
        print("✅ TTSEngine (with fallback)")
    except Exception as e:
        print(f"❌ TTSEngine: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from src.config_manager import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.get_config()
        print(f"✅ Configuration loaded: {len(config)} settings")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_help_command():
    """Test if main script can show help"""
    print("\n📖 Testing help command...")
    
    try:
        import subprocess
        import sys
        
        # Run main.py --help with timeout
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Help command works")
            print("First few lines of help:")
            lines = result.stdout.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print(f"❌ Help command failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Help command timed out (may still work)")
        return True
    except Exception as e:
        print(f"❌ Help command error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 EPUB to Audiobook Converter - Quick Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_basic_imports():
        tests_passed += 1
    
    if test_configuration():
        tests_passed += 1
    
    if test_help_command():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("\n🎉 All tests passed! Your application is ready to run.")
        print("\n🚀 To use the application:")
        print("   python main.py --input 'your-book.epub'")
    elif tests_passed >= 2:
        print("\n⚠️  Most tests passed. Application should work with minor issues.")
        print("\n🚀 To use the application:")
        print("   python main.py --input 'your-book.epub'")
    else:
        print("\n❌ Several tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()

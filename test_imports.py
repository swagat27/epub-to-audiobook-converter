#!/usr/bin/env python3
"""
Quick test script to verify all imports work correctly.
"""

import sys
import traceback

def test_imports():
    """Test all module imports."""
    modules_to_test = [
        ('ebooklib', 'EPUB parsing'),
        ('bs4', 'HTML parsing'),
        ('TTS', 'Text-to-Speech'),
        ('pydub', 'Audio processing'),
        ('torch', 'PyTorch'),
        ('librosa', 'Audio analysis'),
        ('click', 'Command line interface'),
        ('colorama', 'Colored terminal output'),
        ('mutagen', 'Audio metadata'),
        ('numpy', 'Numerical computing'),
        ('soundfile', 'Audio file I/O'),
        ('tqdm', 'Progress bars'),
    ]
    
    print("🔍 Testing imports...")
    print("=" * 50)
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name:<15} - {description}")
        except ImportError as e:
            print(f"❌ {module_name:<15} - {description} (FAILED: {e})")
            failed_imports.append(module_name)
        except Exception as e:
            print(f"⚠️  {module_name:<15} - {description} (ERROR: {e})")
            failed_imports.append(module_name)
    
    print("=" * 50)
    
    # Test project modules
    print("\n🏠 Testing project modules...")
    print("=" * 50)
    
    project_modules = [
        ('src.config_manager', 'Configuration management'),
        ('src.logger', 'Logging setup'),
        ('src.epub_parser', 'EPUB parsing'),
        ('src.text_processor', 'Text processing'),
        ('src.tts_engine', 'TTS engine'),
        ('src.audio_processor', 'Audio processing'),
    ]
    
    for module_name, description in project_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name:<25} - {description}")
        except ImportError as e:
            print(f"❌ {module_name:<25} - {description} (FAILED: {e})")
            failed_imports.append(module_name)
        except Exception as e:
            print(f"⚠️  {module_name:<25} - {description} (ERROR: {e})")
            failed_imports.append(module_name)
    
    print("=" * 50)
    
    if failed_imports:
        print(f"\n❌ {len(failed_imports)} imports failed:")
        for module in failed_imports:
            print(f"   - {module}")
        return False
    else:
        print(f"\n🎉 All imports successful!")
        return True

def test_basic_functionality():
    """Test basic functionality of key components."""
    print("\n🔧 Testing basic functionality...")
    print("=" * 50)
    
    try:
        # Test config manager
        from src.config_manager import ConfigManager
        config = ConfigManager()
        print("✅ ConfigManager - Initialization successful")
        
        # Test TTS availability
        from TTS.api import TTS
        available_models = TTS.list_models()
        print(f"✅ TTS Models - {len(available_models)} models available")
        
        # Test PyTorch GPU availability
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU Support - {torch.cuda.get_device_name()} available")
        else:
            print("ℹ️  GPU Support - CPU only (no CUDA available)")
        
        print("=" * 50)
        print("🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 EPUB to Audiobook Converter - Dependency Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 All tests passed! The application should work correctly.")
            sys.exit(0)
        else:
            print("\n❌ Some functionality tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Some imports failed. Please install missing dependencies.")
        sys.exit(1)

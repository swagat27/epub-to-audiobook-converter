#!/usr/bin/env python3
"""
EPUB to Audiobook Converter - Dependency Setup Script

This script helps install all required dependencies for the project.
"""

import sys
import subprocess
import platform
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3:
        print("❌ Python 3 is required")
        return False
    
    if version.minor < 9:
        print("❌ Python 3.9 or higher is required")
        return False
    
    if version.minor >= 13:
        print("⚠️  Warning: Python 3.13+ may have compatibility issues with some packages")
        print("   Consider using Python 3.11 or 3.12 for best compatibility")
    
    return True

def check_package(package_name, import_name=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip."""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def install_pytorch():
    """Install PyTorch with appropriate version."""
    print("🔥 Installing PyTorch...")
    try:
        if platform.system() == "Windows":
            # Install CPU version for Windows
            cmd = [sys.executable, "-m", "pip", "install", "torch", "torchaudio", 
                   "--index-url", "https://download.pytorch.org/whl/cpu"]
        else:
            cmd = [sys.executable, "-m", "pip", "install", "torch", "torchaudio"]
        
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyTorch: {e}")
        return False

def install_tts():
    """Install TTS (Coqui-TTS) with fallbacks."""
    print("🎤 Installing TTS (Coqui-TTS)...")
    
    # Try different installation methods
    attempts = [
        "TTS",
        "coqui-tts",
        "TTS>=0.21.0",
        "TTS>=0.20.0"
    ]
    
    for attempt in attempts:
        try:
            print(f"   Trying: {attempt}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", attempt])
            
            # Test if import works
            try:
                import TTS
                print("✅ TTS installed successfully!")
                return True
            except ImportError:
                continue
                
        except subprocess.CalledProcessError:
            continue
    
    print("❌ Failed to install TTS. You may need to:")
    print("   1. Use a different Python version (3.9-3.12)")
    print("   2. Install from source")
    print("   3. Use a virtual environment")
    return False

def check_ffmpeg():
    """Check if FFmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found")
        print("   Download from: https://ffmpeg.org/download.html")
        print("   Add to your system PATH")
        return False

def main():
    """Main setup function."""
    print("🚀 EPUB to Audiobook Converter - Dependency Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📋 Checking current dependencies...")
    
    # Core dependencies to check/install
    dependencies = [
        ("ebooklib", "ebooklib"),
        ("beautifulsoup4", "bs4"),
        ("lxml", "lxml"),
        ("pydub", "pydub"),
        ("click", "click"),
        ("colorama", "colorama"),
        ("tqdm", "tqdm"),
        ("mutagen", "mutagen"),
        ("numpy", "numpy"),
        ("librosa", "librosa"),
        ("soundfile", "soundfile"),
    ]
    
    missing_packages = []
    
    for package, import_name in dependencies:
        if check_package(package, import_name):
            print(f"✅ {package}")
        else:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    # Check PyTorch separately
    if check_package("torch"):
        print("✅ torch (PyTorch)")
    else:
        print("❌ torch (PyTorch) - Missing")
        missing_packages.append("torch")
    
    # Check TTS separately
    if check_package("TTS", "TTS.api"):
        print("✅ TTS (Coqui-TTS)")
    else:
        print("❌ TTS (Coqui-TTS) - Missing")
        missing_packages.append("TTS")
    
    # Check FFmpeg
    check_ffmpeg()
    
    if not missing_packages:
        print("\n🎉 All dependencies are installed!")
        return
    
    print(f"\n📦 Installing {len(missing_packages)} missing packages...")
    
    # Install regular packages
    regular_packages = [pkg for pkg in missing_packages if pkg not in ["torch", "TTS"]]
    if regular_packages:
        for package in regular_packages:
            install_package(package)
    
    # Install PyTorch if missing
    if "torch" in missing_packages:
        install_pytorch()
    
    # Install TTS if missing
    if "TTS" in missing_packages:
        install_tts()
    
    print("\n🧪 Testing final installation...")
    
    # Test imports
    test_packages = [
        ("ebooklib", "ebooklib"),
        ("beautifulsoup4", "bs4"),
        ("torch", "torch"),
        ("TTS", "TTS.api"),
        ("pydub", "pydub"),
    ]
    
    all_good = True
    for package, import_name in test_packages:
        try:
            importlib.import_module(import_name)
            print(f"✅ {package} - Working")
        except ImportError:
            print(f"❌ {package} - Still missing")
            all_good = False
    
    if all_good:
        print("\n🎉 Setup complete! You can now run:")
        print("   python main.py --help")
    else:
        print("\n⚠️  Some packages are still missing.")
        print("   You may need to install them manually or use a different Python version.")

if __name__ == "__main__":
    main()

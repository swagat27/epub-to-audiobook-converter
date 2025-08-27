# EPUB to Audiobook Converter

A comprehensive Python application that converts EPUB eBooks into high-quality audiobooks using advanced text-to-speech technology with GPU acceleration support.

## 🚀 Quick Start

**New to this project? Start here:**

```bash
# 1. Check if everything is ready
python check_setup.py

# 2. Install dependencies if needed
./install.sh        # Linux/macOS
# OR
install.bat         # Windows

# 3. Use the interactive helper
python run.py

# 4. Or run directly
python main.py -i "path/to/book.epub"
```

**Having issues?** See [HOW_TO_RUN.md](HOW_TO_RUN.md) for a step-by-step guide.

## Features

- **EPUB Parsing**: Extracts text content and metadata from EPUB files chapter by chapter
- **High-Quality TTS**: Uses Coqui TTS engine with multiple language and voice support
- **GPU Acceleration**: Optional CUDA support for faster processing
- **Multiple Output Formats**: Supports M4B and MP3 audiobook formats
- **Metadata Management**: Automatically adds book metadata and chapter markers
- **Text Processing**: Advanced text cleaning and normalization for optimal speech synthesis
- **Command-Line Interface**: Easy-to-use CLI with comprehensive options
- **Progress Tracking**: Real-time progress updates and detailed logging
- **Configurable Settings**: Extensive configuration options for customization

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Optional: CUDA-compatible GPU for acceleration

### Install Dependencies

```bash
# Clone or download the project
cd epub_to_audiobook

# Install Python dependencies
pip install -r requirements.txt

# For GPU acceleration (optional)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### System Dependencies

#### Windows
- Install FFmpeg: Download from https://ffmpeg.org/download.html
- Add FFmpeg to your system PATH

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg libsndfile1-dev
```

## How to Run This Application

This guide will help you get the EPUB to Audiobook Converter up and running on your system.

### Prerequisites

- **Python 3.8 to 3.11** (TTS library has compatibility issues with Python 3.12+)
- **pip** package manager
- **FFmpeg** (for audio processing)
- **Git** (to clone the repository)

### Step 1: Download/Clone the Repository

```bash
# Clone the repository
git clone https://github.com/swagat27/epub-to-audiobook-converter.git
cd epub-to-audiobook-converter
```

### Step 2: Install Dependencies

#### Option A: Automatic Installation (Recommended)

**For Unix/Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**For Windows:**
```cmd
install.bat
```

#### Option B: Manual Installation

**1. Install basic dependencies:**
```bash
pip install -r requirements-basic.txt
```

**2. Install TTS and audio dependencies:**
```bash
# For Python 3.8-3.11
pip install TTS pydub mutagen numpy librosa soundfile

# For GPU acceleration (optional)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**3. Install system dependencies:**

- **Windows**: Download FFmpeg from https://ffmpeg.org and add to PATH
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg libsndfile1-dev`

### Step 3: Prepare Your EPUB Files

```bash
# Create input directory and place your EPUB files
mkdir -p input
# Copy your .epub files to the input/ directory
```

### Step 4: Run the Application

#### Basic Usage

```bash
# Convert an EPUB to audiobook
python main.py -i "input/your_book.epub"

# The audiobook will be created in the output/ directory
```

#### Try the Demo (No TTS Dependencies Required)

If you're having trouble with TTS installation, try the demo first:

```bash
python demo.py -i "input/your_book.epub"
```

This will parse the EPUB and show you the extracted text without creating audio.

### Step 5: Common Usage Examples

```bash
# Basic conversion with default settings
python main.py -i "input/book.epub"

# Specify output directory and format
python main.py -i "input/book.epub" -o "my_audiobooks" -f mp3

# Use GPU acceleration for faster processing
python main.py -i "input/book.epub" --gpu

# Adjust speech settings
python main.py -i "input/book.epub" --speed 1.2 --pitch 0.9

# Use different voice/language
python main.py -i "input/book.epub" -v es  # Spanish voice

# Enable debug logging
python main.py -i "input/book.epub" --log-level DEBUG
```

### Troubleshooting

#### Python Version Issues

If you have Python 3.12+, the TTS library may not install. Solutions:

1. **Use Python 3.11**: Install Python 3.11 and create a virtual environment
2. **Try force installation**: `pip install TTS --no-deps --force-reinstall`
3. **Use the demo version**: `python demo.py` works without TTS dependencies

#### Missing Dependencies

```bash
# If you get "ModuleNotFoundError"
pip install -r requirements-basic.txt

# For audio processing errors
pip install pydub mutagen soundfile

# For TTS errors
pip install TTS
```

#### FFmpeg Not Found

- **Windows**: Download from https://ffmpeg.org and add to system PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent for your distro

#### GPU Issues

```bash
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Install CPU-only version if GPU issues persist
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Getting Help

```bash
# View all available options
python main.py --help

# View example usage
python examples.py

# Check the logs for detailed error information
cat logs/epub_to_audiobook.log
```

## Quick Start

### Basic Usage

```bash
# Convert an EPUB file to audiobook
python main.py -i "path/to/book.epub" -o "./output"

# Specify voice and format
python main.py -i "book.epub" -v en -f m4b --gpu

# Use custom settings
python main.py -i "book.epub" --speed 1.2 --pitch 0.9 --chapter-pause 3.0
```

### Command-Line Options

```
Options:
  -i, --input PATH          Path to input EPUB file [required]
  -o, --output PATH         Output directory [default: ./output]
  -v, --voice TEXT          Voice/language for TTS [default: en]
  -s, --speaker TEXT        Speaker voice style [default: default]
  --speed FLOAT            Speech speed multiplier [default: 1.0]
  --pitch FLOAT            Pitch multiplier [default: 1.0]
  -f, --format [mp3|m4b]   Output audio format [default: m4b]
  --gpu                    Enable GPU acceleration
  -c, --config PATH        Path to configuration file
  --log-level [DEBUG|INFO|WARNING|ERROR]  Logging level [default: INFO]
  --chapter-pause FLOAT    Pause between chapters in seconds [default: 2.0]
  --help                   Show this message and exit
```

## Configuration

### Configuration File

Create a JSON configuration file for advanced settings:

```json
{
  "tts_settings": {
    "tts_model": "tts_models/en/ljspeech/tacotron2-DDC",
    "voice": "en",
    "speaker": "default",
    "speed": 1.0,
    "pitch": 1.0,
    "gpu_acceleration": false
  },
  "audio_settings": {
    "output_format": "m4b",
    "audio_quality": "high",
    "chapter_pause": 2.0
  },
  "processing_settings": {
    "max_chunk_length": 500,
    "max_workers": 2,
    "cleanup_temp": true
  }
}
```

### Environment Variables

Override settings using environment variables:

```bash
export EPUB_GPU=true
export EPUB_FORMAT=m4b
export EPUB_VOICE=en
export EPUB_SPEED=1.2
export EPUB_OUTPUT_DIR="./my_audiobooks"
```

## Supported Languages

The application supports multiple languages with optimized TTS models:

- English (en) - Default
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)

## Project Structure

```
epub_to_audiobook/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code modules
│   ├── epub_parser.py     # EPUB file parsing
│   ├── text_processor.py  # Text cleaning and processing
│   ├── tts_engine.py      # Text-to-speech engine
│   ├── audio_processor.py # Audio processing and merging
│   ├── config_manager.py  # Configuration management
│   └── logger.py          # Logging utilities
├── input/                 # Input EPUB files (place your books here)
├── output/                # Generated audiobooks
├── config/                # Configuration files
├── logs/                  # Application logs
└── .vscode/               # VS Code configuration
    └── tasks.json         # Build and run tasks
```

## Examples

### Convert with Custom Voice Settings

```bash
# High-quality conversion with GPU acceleration
python main.py \
  --input "My_Book.epub" \
  --output "./audiobooks" \
  --voice en \
  --speed 1.1 \
  --pitch 0.95 \
  --format m4b \
  --gpu \
  --log-level INFO
```

### Batch Processing

```bash
# Process multiple books (create a script)
for book in input/*.epub; do
    python main.py -i "$book" -o "./output" --gpu
done
```

### Using Configuration File

```bash
# Use custom configuration
python main.py -i "book.epub" -c "./config/custom_config.json"
```

## Performance Tips

### GPU Acceleration
- Install CUDA-compatible PyTorch for significant speed improvements
- Use `--gpu` flag to enable GPU acceleration
- Monitor GPU memory usage for large books

### CPU Optimization
- Adjust `max_workers` in configuration for your CPU core count
- Use higher quality settings only when necessary
- Enable temporary file cleanup to save disk space

### Memory Management
- For very large books, consider splitting into smaller sections
- Monitor memory usage with the built-in logging
- Adjust batch size in configuration if needed

## Troubleshooting

### Common Issues

1. **Import Errors**: Install all dependencies with `pip install -r requirements.txt`
2. **GPU Not Detected**: Ensure CUDA-compatible PyTorch is installed
3. **Audio Quality Issues**: Try different TTS models or adjust quality settings
4. **Memory Errors**: Reduce batch size or disable GPU acceleration
5. **File Format Issues**: Ensure input file is a valid EPUB

### Debug Mode

Enable debug logging for detailed information:

```bash
python main.py -i "book.epub" --log-level DEBUG
```

### Logs

Check the logs directory for detailed execution logs:
- `logs/epub_to_audiobook.log` - Main application log
- Console output for real-time progress

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black src/ main.py

# Type checking
mypy src/
```

### Code Structure

The application is modular with separate components for:
- EPUB parsing and text extraction
- Text cleaning and normalization
- TTS engine management
- Audio processing and merging
- Configuration and logging

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Coqui TTS](https://github.com/coqui-ai/TTS) for the excellent text-to-speech engine
- [EbookLib](https://github.com/aerkalov/ebooklib) for EPUB parsing capabilities
- [PyDub](https://github.com/jiaaro/pydub) for audio processing
- [Mutagen](https://github.com/quodlibet/mutagen) for metadata management

## Support

For support, feature requests, or bug reports:
1. Check the existing issues in the repository
2. Create a new issue with detailed information
3. Include logs and system information for bugs

## Roadmap

- [ ] Support for additional ebook formats (MOBI, AZW3)
- [ ] Voice cloning capabilities
- [ ] Web interface for easier usage
- [ ] Docker containerization
- [ ] Cloud processing support
- [ ] Advanced audio post-processing
- [ ] Multi-language document support
- [ ] Automated book detection and metadata fetching

---

**Note**: This application is for personal use only. Please respect copyright laws and only convert books you own or have permission to convert.

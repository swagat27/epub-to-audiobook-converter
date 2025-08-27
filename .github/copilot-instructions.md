<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# EPUB to Audiobook Converter - Copilot Instructions

This is a Python application for converting EPUB eBooks into audiobooks using text-to-speech technology.

## Project Context

- **Main Purpose**: Convert EPUB files to audiobooks (M4B/MP3) using TTS
- **Key Technologies**: Python, Coqui TTS, PyTorch, PyDub, EbookLib
- **Architecture**: Modular design with separate components for parsing, processing, TTS, and audio handling
- **Target Users**: Book enthusiasts, accessibility users, content creators

## Code Style Guidelines

- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all classes and functions
- Prefer descriptive variable names over comments
- Use logging instead of print statements for output
- Handle exceptions gracefully with proper error logging

## Key Components

1. **epub_parser.py**: Handles EPUB file parsing and text extraction
2. **text_processor.py**: Cleans and normalizes text for optimal TTS
3. **tts_engine.py**: Manages text-to-speech conversion with GPU support
4. **audio_processor.py**: Handles audio merging and metadata addition
5. **config_manager.py**: Manages application configuration
6. **logger.py**: Provides comprehensive logging functionality

## Development Guidelines

- Always include error handling for file operations and external API calls
- Use configuration-driven approach for settings and parameters
- Implement progress tracking for long-running operations
- Support both CPU and GPU processing modes
- Ensure cross-platform compatibility (Windows, macOS, Linux)
- Add comprehensive logging at appropriate levels (DEBUG, INFO, WARNING, ERROR)

## Dependencies

- Core: ebooklib, beautifulsoup4, TTS, pydub, click, torch
- Audio: mutagen, soundfile, librosa
- Utilities: colorama, tqdm, numpy

## When suggesting code improvements:

- Prioritize performance optimization for large files
- Consider memory efficiency for batch processing
- Suggest GPU acceleration opportunities where applicable
- Recommend error recovery mechanisms
- Focus on user experience and progress feedback
- Ensure compatibility with various EPUB formats and structures

## Testing Considerations

- Test with various EPUB file formats and structures
- Verify audio quality and metadata preservation
- Test both CPU and GPU processing paths
- Validate configuration file handling
- Check error handling for edge cases (corrupted files, network issues, etc.)

## Security Guidelines

- Validate all file paths and user inputs
- Sanitize filenames and metadata
- Handle temporary files securely
- Avoid exposing sensitive system information in logs

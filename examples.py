#!/usr/bin/env python3
"""
Example usage script for the EPUB to Audiobook Converter.
This script demonstrates various ways to use the converter programmatically.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.epub_parser import EPUBParser
from src.text_processor import TextProcessor
from src.tts_engine import TTSEngine
from src.audio_processor import AudioProcessor
from src.config_manager import ConfigManager
from src.logger import setup_logger

def example_basic_conversion():
    """Example of basic EPUB to audiobook conversion."""
    print("=== Basic Conversion Example ===")
    
    # Setup logging
    logger = setup_logger("example", "INFO")
    
    # Configuration
    config = {
        'voice': 'en',
        'speaker': 'default',
        'speed': 1.0,
        'pitch': 1.0,
        'gpu_acceleration': False,
        'output_format': 'm4b',
        'chapter_pause': 2.0
    }
    
    # Initialize components
    epub_parser = EPUBParser()
    text_processor = TextProcessor()
    tts_engine = TTSEngine(config)
    audio_processor = AudioProcessor(config)
    
    # Example EPUB file path (you would replace this with an actual file)
    epub_path = "input/sample.epub"
    output_dir = "output"
    
    if not os.path.exists(epub_path):
        logger.warning(f"Sample EPUB file not found: {epub_path}")
        logger.info("Please place an EPUB file in the input directory to test")
        return
    
    try:
        # Parse EPUB
        logger.info("Parsing EPUB file...")
        book_data = epub_parser.parse_epub(epub_path)
        
        # Process chapters
        audio_files = []
        for i, chapter in enumerate(book_data['chapters'][:2]):  # Process only first 2 chapters for demo
            logger.info(f"Processing chapter {i+1}: {chapter['title']}")
            
            # Clean text
            processed_text = text_processor.clean_text(chapter['content'])
            
            # Generate audio
            if processed_text.strip():
                audio_file = tts_engine.text_to_speech(
                    processed_text[:500],  # Limit text for demo
                    chapter['title'],
                    output_dir,
                    chapter_num=i+1
                )
                
                if audio_file:
                    audio_files.append({
                        'file': audio_file,
                        'title': chapter['title'],
                        'chapter_num': i+1
                    })
        
        # Merge into audiobook
        if audio_files:
            logger.info("Creating audiobook...")
            output_file = audio_processor.merge_audiobook(audio_files, book_data, output_dir)
            
            if output_file:
                logger.info(f"Audiobook created: {output_file}")
            else:
                logger.error("Failed to create audiobook")
        
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
    
    finally:
        # Cleanup
        tts_engine.cleanup()

def example_configuration_usage():
    """Example of using configuration files."""
    print("\n=== Configuration Example ===")
    
    # Create configuration manager
    config_manager = ConfigManager()
    
    # Show default configuration
    print("Default configuration keys:")
    for key in sorted(config_manager.get_config().keys()):
        print(f"  - {key}")
    
    # Create sample configuration file
    sample_config_path = "config/example_config.json"
    config_manager.create_sample_config(sample_config_path)
    print(f"\nSample configuration created: {sample_config_path}")
    
    # Load configuration from file
    config_with_file = ConfigManager(sample_config_path)
    print("Configuration loaded from file successfully")

def example_text_processing():
    """Example of text processing capabilities."""
    print("\n=== Text Processing Example ===")
    
    processor = TextProcessor()
    
    # Sample text with various issues
    sample_text = """
    Dr. Smith said, "The U.S.A. is great!" 
    He visited http://example.com and sent an email to test@example.com.
    The temperature was 25°C (77°F).
    This costs $19.99 vs. €15.50.
    """
    
    print("Original text:")
    print(repr(sample_text))
    
    # Clean the text
    cleaned_text = processor.clean_text(sample_text)
    print("\nCleaned text:")
    print(repr(cleaned_text))
    
    # Get text statistics
    stats = processor.get_text_statistics(cleaned_text)
    print(f"\nText statistics: {stats}")
    
    # Split into chunks
    chunks = processor.split_into_chunks(cleaned_text, max_length=50)
    print(f"\nText chunks: {chunks}")

def example_epub_info():
    """Example of getting EPUB information without full processing."""
    print("\n=== EPUB Information Example ===")
    
    parser = EPUBParser()
    epub_path = "input/sample.epub"
    
    if os.path.exists(epub_path):
        info = parser.get_book_info(epub_path)
        print("Book information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print(f"Sample EPUB not found: {epub_path}")
        print("Please place an EPUB file in the input directory")

def main():
    """Run all examples."""
    print("EPUB to Audiobook Converter - Examples")
    print("="*50)
    
    # Create directories if they don't exist
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    try:
        # Run examples
        example_configuration_usage()
        example_text_processing()
        example_epub_info()
        
        # Only run conversion if we have the required dependencies
        try:
            import torch
            import TTS
            example_basic_conversion()
        except ImportError as e:
            print(f"\nSkipping conversion example due to missing dependencies: {e}")
            print("Install all requirements with: pip install -r requirements.txt")
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
    
    print("\nExamples completed!")

if __name__ == "__main__":
    main()

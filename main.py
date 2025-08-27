"""
EPUB to Audiobook Converter

A comprehensive Python application that converts EPUB eBooks into high-quality audiobooks
using advanced text-to-speech technology with GPU acceleration support.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

import click
from colorama import init, Fore, Style

# Try to import dependencies gracefully
try:
    from src.epub_parser import EPUBParser
    EPUB_PARSER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: EPUB parser not available: {e}")
    EPUB_PARSER_AVAILABLE = False

try:
    from src.text_processor import TextProcessor
    TEXT_PROCESSOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Text processor not available: {e}")
    TEXT_PROCESSOR_AVAILABLE = False

try:
    from src.tts_engine import TTSEngine
    TTS_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: TTS engine not available: {e}")
    TTS_ENGINE_AVAILABLE = False

try:
    from src.audio_processor import AudioProcessor
    AUDIO_PROCESSOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Audio processor not available: {e}")
    AUDIO_PROCESSOR_AVAILABLE = False

try:
    from src.config_manager import ConfigManager
    CONFIG_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Config manager not available: {e}")
    CONFIG_MANAGER_AVAILABLE = False

try:
    from src.logger import setup_logger
    LOGGER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Logger not available: {e}")
    LOGGER_AVAILABLE = False

# Initialize colorama for cross-platform colored output
init()

def check_dependencies():
    """Check which dependencies are available and show status."""
    click.echo(f"\n{Fore.CYAN}📋 Dependency Status Check{Style.RESET_ALL}")
    click.echo("=" * 50)
    
    dependencies = [
        ("EPUB Parser", EPUB_PARSER_AVAILABLE),
        ("Text Processor", TEXT_PROCESSOR_AVAILABLE),
        ("TTS Engine", TTS_ENGINE_AVAILABLE),
        ("Audio Processor", AUDIO_PROCESSOR_AVAILABLE),
        ("Config Manager", CONFIG_MANAGER_AVAILABLE),
        ("Logger", LOGGER_AVAILABLE),
    ]
    
    all_available = True
    for name, available in dependencies:
        status = f"{Fore.GREEN}✓ Available{Style.RESET_ALL}" if available else f"{Fore.RED}✗ Missing{Style.RESET_ALL}"
        click.echo(f"{name:20} : {status}")
        if not available:
            all_available = False
    
    click.echo()
    if all_available:
        click.echo(f"{Fore.GREEN}🎉 All dependencies are available!{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.YELLOW}⚠️  Some dependencies are missing. Install them with:{Style.RESET_ALL}")
        click.echo(f"   pip install -r requirements.txt")
        click.echo()
        click.echo(f"{Fore.CYAN}ℹ️  You can still run examples and basic functionality.{Style.RESET_ALL}")
    
    return all_available


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup application logging."""
    if LOGGER_AVAILABLE:
        return setup_logger("epub_to_audiobook", log_level)
    else:
        # Fallback to basic logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger("epub_to_audiobook")

@click.group()
def cli():
    """EPUB to Audiobook Converter CLI"""
    pass

@cli.command()
def check():
    """Check dependency status and system requirements."""
    check_dependencies()

@cli.command()
@click.option('--input', '-i', 'input_path', required=True, 
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to the input EPUB file')
@click.option('--output', '-o', 'output_dir', 
              type=click.Path(file_okay=False, dir_okay=True),
              default='./output',
              help='Output directory for the audiobook (default: ./output)')
@click.option('--voice', '-v', default='en',
              help='Voice/language for TTS (default: en)')
@click.option('--speaker', '-s', default='default',
              help='Speaker voice style (default: default)')
@click.option('--speed', default=1.0, type=float,
              help='Speech speed multiplier (default: 1.0)')
@click.option('--pitch', default=1.0, type=float,
              help='Pitch multiplier (default: 1.0)')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['mp3', 'm4b'], case_sensitive=False),
              default='m4b',
              help='Output audio format (default: m4b)')
@click.option('--gpu', is_flag=True, default=False,
              help='Enable GPU acceleration for TTS processing')
@click.option('--config', '-c', 'config_file',
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to configuration file')
@click.option('--log-level', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
              default='INFO',
              help='Logging level (default: INFO)')
@click.option('--chapter-pause', default=2.0, type=float,
              help='Pause duration between chapters in seconds (default: 2.0)')
def convert(input_path: str, output_dir: str, voice: str, speaker: str, 
         speed: float, pitch: float, output_format: str, gpu: bool,
         config_file: Optional[str], log_level: str, chapter_pause: float):
    """
    Convert EPUB eBooks to audiobooks using advanced text-to-speech technology.
    
    This application parses EPUB files chapter by chapter, converts text to speech
    using high-quality TTS engines, and merges the audio into a single audiobook file
    with proper metadata and chapter markers.
    """
    
    # Setup logging
    logger = setup_logging(log_level.upper())
    
    try:
        # Print welcome message
        click.echo(f"\n{Fore.CYAN}📚 EPUB to Audiobook Converter{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Converting: {input_path}{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}Output: {output_dir}{Style.RESET_ALL}\n")
        
        # Check dependencies first
        all_deps_available = check_dependencies()
        if not all_deps_available:
            click.echo(f"\n{Fore.RED}❌ Cannot proceed with conversion due to missing dependencies.{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}💡 Try running the examples script to see what's available:{Style.RESET_ALL}")
            click.echo(f"   python examples.py")
            return
        
        # Load configuration
        if not CONFIG_MANAGER_AVAILABLE:
            logger.error("Config manager not available")
            return
            
        config_manager = ConfigManager(config_file)
        config = config_manager.get_config()
        
        # Override config with command line arguments
        config.update({
            'voice': voice,
            'speaker': speaker,
            'speed': speed,
            'pitch': pitch,
            'gpu_acceleration': gpu,
            'output_format': output_format.lower(),
            'chapter_pause': chapter_pause
        })
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        epub_parser = EPUBParser()
        text_processor = TextProcessor()
        tts_engine = TTSEngine(config)
        audio_processor = AudioProcessor(config)
        
        # Parse EPUB file
        logger.info("Parsing EPUB file...")
        book_data = epub_parser.parse_epub(input_path)
        
        if not book_data['chapters']:
            logger.error("No chapters found in EPUB file")
            return
        
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Found {len(book_data['chapters'])} chapters")
        
        # Process each chapter
        audio_files = []
        total_chapters = len(book_data['chapters'])
        
        with click.progressbar(book_data['chapters'], label='Converting chapters') as chapters:
            for i, chapter in enumerate(chapters):
                logger.info(f"Processing chapter {i+1}/{total_chapters}: {chapter['title']}")
                
                # Clean and process text
                processed_text = text_processor.clean_text(chapter['content'])
                
                if not processed_text.strip():
                    logger.warning(f"Chapter {i+1} has no content, skipping...")
                    continue
                
                # Generate audio for chapter
                audio_file = tts_engine.text_to_speech(
                    processed_text, 
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
        
        if not audio_files:
            logger.error("No audio files were generated")
            return
        
        click.echo(f"\n{Fore.GREEN}✓{Style.RESET_ALL} Generated {len(audio_files)} audio files")
        
        # Merge audio files into final audiobook
        logger.info("Merging audio files into audiobook...")
        output_file = audio_processor.merge_audiobook(
            audio_files, 
            book_data, 
            output_dir
        )
        
        if output_file:
            click.echo(f"\n{Fore.GREEN}🎉 Audiobook created successfully!{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}Output file: {output_file}{Style.RESET_ALL}")
            
            # Display file info
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            click.echo(f"{Fore.YELLOW}File size: {file_size:.2f} MB{Style.RESET_ALL}")
        else:
            logger.error("Failed to create audiobook")
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        click.echo(f"\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        click.echo(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    cli()

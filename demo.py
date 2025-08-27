#!/usr/bin/env python3
"""
Demo version of the EPUB to Audiobook Converter.
This version demonstrates the core functionality without TTS dependencies.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

import click
from colorama import init, Fore, Style

from src.epub_parser import EPUBParser
from src.text_processor import TextProcessor
from src.config_manager import ConfigManager
from src.logger import setup_logger

# Initialize colorama for cross-platform colored output
init()

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup application logging."""
    return setup_logger("epub_demo", log_level)

@click.command()
@click.option('--input', '-i', 'input_path', required=True, 
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to the input EPUB file')
@click.option('--output', '-o', 'output_dir', 
              type=click.Path(file_okay=False, dir_okay=True),
              default='./output',
              help='Output directory for the text files (default: ./output)')
@click.option('--log-level', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
              default='INFO',
              help='Logging level (default: INFO)')
def main(input_path: str, output_dir: str, log_level: str):
    """
    Demo: Parse EPUB files and extract clean text (without TTS conversion).
    
    This demo version shows the text extraction and cleaning capabilities
    without requiring the heavy TTS dependencies.
    """
    
    # Setup logging
    logger = setup_logging(log_level.upper())
    
    try:
        # Print welcome message
        click.echo(f"\n{Fore.CYAN}📚 EPUB Parser Demo{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Parsing: {input_path}{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}Output: {output_dir}{Style.RESET_ALL}\n")
        
        # Load configuration (basic version)
        config_manager = ConfigManager()
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        epub_parser = EPUBParser()
        text_processor = TextProcessor()
        
        # Parse EPUB file
        logger.info("Parsing EPUB file...")
        book_data = epub_parser.parse_epub(input_path)
        
        if not book_data['chapters']:
            logger.error("No chapters found in EPUB file")
            return
        
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Found {len(book_data['chapters'])} chapters")
        
        # Display book metadata
        metadata = book_data['metadata']
        click.echo(f"\n{Fore.CYAN}Book Information:{Style.RESET_ALL}")
        click.echo(f"  Title: {metadata.get('title', 'Unknown')}")
        click.echo(f"  Author: {metadata.get('author', 'Unknown')}")
        click.echo(f"  Language: {metadata.get('language', 'Unknown')}")
        if metadata.get('description'):
            desc = metadata['description'][:100] + "..." if len(metadata['description']) > 100 else metadata['description']
            click.echo(f"  Description: {desc}")
        
        # Process each chapter
        total_words = 0
        total_chapters = len(book_data['chapters'])
        
        click.echo(f"\n{Fore.CYAN}Processing Chapters:{Style.RESET_ALL}")
        
        with click.progressbar(book_data['chapters'], label='Processing chapters') as chapters:
            for i, chapter in enumerate(chapters):
                logger.info(f"Processing chapter {i+1}/{total_chapters}: {chapter['title']}")
                
                # Clean and process text
                processed_text = text_processor.clean_text(chapter['content'])
                
                if not processed_text.strip():
                    logger.warning(f"Chapter {i+1} has no content, skipping...")
                    continue
                
                # Get text statistics
                stats = text_processor.get_text_statistics(processed_text)
                total_words += stats['words']
                
                # Save processed text to file
                safe_title = text_processor._create_safe_filename(chapter['title']) if hasattr(text_processor, '_create_safe_filename') else f"chapter_{i+1:03d}"
                output_file = os.path.join(output_dir, f"chapter_{i+1:03d}_{safe_title}.txt")
                
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Chapter {i+1}: {chapter['title']}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(processed_text)
                        f.write(f"\n\n--- Chapter Statistics ---\n")
                        f.write(f"Words: {stats['words']}\n")
                        f.write(f"Characters: {stats['characters']}\n")
                        f.write(f"Sentences: {stats['sentences']}\n")
                    
                    logger.debug(f"Saved chapter to: {output_file}")
                    
                except Exception as e:
                    logger.error(f"Error saving chapter {i+1}: {str(e)}")
        
        # Create summary file
        summary_file = os.path.join(output_dir, "book_summary.txt")
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"EPUB Book Summary\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Title: {metadata.get('title', 'Unknown')}\n")
                f.write(f"Author: {metadata.get('author', 'Unknown')}\n")
                f.write(f"Language: {metadata.get('language', 'Unknown')}\n")
                f.write(f"Total Chapters: {total_chapters}\n")
                f.write(f"Total Words: {total_words:,}\n")
                f.write(f"Estimated Reading Time: {text_processor.estimate_reading_time(' ' * total_words):.1f} minutes\n")
                
                if metadata.get('description'):
                    f.write(f"\nDescription:\n{metadata['description']}\n")
                
                f.write(f"\nChapter List:\n")
                for i, chapter in enumerate(book_data['chapters'], 1):
                    f.write(f"{i:3d}. {chapter['title']} ({chapter['word_count']} words)\n")
            
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Summary saved to: {summary_file}")
            
        except Exception as e:
            logger.error(f"Error creating summary: {str(e)}")
        
        click.echo(f"\n{Fore.GREEN}🎉 Processing completed successfully!{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Processed {total_chapters} chapters with {total_words:,} total words{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Text files saved to: {output_dir}{Style.RESET_ALL}")
        
        # Show next steps
        click.echo(f"\n{Fore.CYAN}Next Steps:{Style.RESET_ALL}")
        click.echo("1. Install TTS dependencies: pip install -r requirements.txt")
        click.echo("2. Use main.py for full audiobook conversion")
        click.echo("3. Run examples.py to see more features")
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        click.echo(f"\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        click.echo(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main()

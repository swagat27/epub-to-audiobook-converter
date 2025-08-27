"""
EPUB Parser Module

Handles parsing of EPUB files to extract text content and metadata.
"""

import os
import zipfile
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class EPUBParser:
    """
    Parser for EPUB files that extracts chapters, metadata, and content.
    """
    
    def __init__(self):
        self.supported_formats = ['.epub']
    
    def parse_epub(self, epub_path: str) -> Dict[str, Any]:
        """
        Parse an EPUB file and extract all relevant information.
        
        Args:
            epub_path (str): Path to the EPUB file
            
        Returns:
            Dict containing book metadata and chapters
        """
        try:
            # Validate file
            if not self._validate_epub_file(epub_path):
                raise ValueError(f"Invalid EPUB file: {epub_path}")
            
            # Read EPUB
            book = epub.read_epub(epub_path)
            
            # Extract metadata
            metadata = self._extract_metadata(book)
            
            # Extract chapters
            chapters = self._extract_chapters(book)
            
            # Get cover image if available
            cover_image = self._extract_cover_image(book)
            
            book_data = {
                'metadata': metadata,
                'chapters': chapters,
                'cover_image': cover_image,
                'total_chapters': len(chapters),
                'file_path': epub_path
            }
            
            logger.info(f"Successfully parsed EPUB: {metadata.get('title', 'Unknown')}")
            logger.info(f"Found {len(chapters)} chapters")
            
            return book_data
            
        except Exception as e:
            logger.error(f"Error parsing EPUB file: {str(e)}")
            raise
    
    def _validate_epub_file(self, epub_path: str) -> bool:
        """Validate if the file is a proper EPUB file."""
        try:
            if not os.path.exists(epub_path):
                return False
            
            if not epub_path.lower().endswith('.epub'):
                return False
            
            # Try to open as zip file (EPUB is essentially a zip)
            with zipfile.ZipFile(epub_path, 'r') as zip_file:
                # Check for mimetype file
                if 'mimetype' in zip_file.namelist():
                    mimetype = zip_file.read('mimetype').decode('utf-8').strip()
                    return mimetype == 'application/epub+zip'
            
            return False
            
        except Exception:
            return False
    
    def _extract_metadata(self, book: epub.EpubBook) -> Dict[str, str]:
        """Extract metadata from EPUB book."""
        metadata = {}
        
        try:
            # Basic metadata
            metadata['title'] = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Unknown Title'
            metadata['author'] = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Unknown Author'
            metadata['language'] = book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else 'en'
            metadata['publisher'] = book.get_metadata('DC', 'publisher')[0][0] if book.get_metadata('DC', 'publisher') else ''
            metadata['date'] = book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else ''
            metadata['description'] = book.get_metadata('DC', 'description')[0][0] if book.get_metadata('DC', 'description') else ''
            metadata['subject'] = book.get_metadata('DC', 'subject')[0][0] if book.get_metadata('DC', 'subject') else ''
            
            # Clean up metadata
            for key, value in metadata.items():
                if isinstance(value, str):
                    metadata[key] = value.strip()
            
        except Exception as e:
            logger.warning(f"Error extracting some metadata: {str(e)}")
        
        return metadata
    
    def _extract_chapters(self, book: epub.EpubBook) -> List[Dict[str, Any]]:
        """Extract chapters from EPUB book in correct order."""
        chapters = []
        
        try:
            # Get the spine (reading order)
            spine_items = [item[0] for item in book.spine if item[1] == 'yes']
            
            chapter_num = 1
            for item_id in spine_items:
                item = book.get_item_with_id(item_id)
                
                if item and hasattr(item, 'get_content'):
                    content = item.get_content()
                    
                    if content:
                        # Parse HTML content
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extract title
                        title = self._extract_chapter_title(soup, chapter_num)
                        
                        # Extract text content
                        text_content = self._extract_text_content(soup)
                        
                        if text_content.strip():  # Only add chapters with content
                            chapters.append({
                                'title': title,
                                'content': text_content,
                                'chapter_num': chapter_num,
                                'item_id': item_id,
                                'word_count': len(text_content.split())
                            })
                            chapter_num += 1
            
        except Exception as e:
            logger.error(f"Error extracting chapters: {str(e)}")
            raise
        
        return chapters
    
    def _extract_chapter_title(self, soup: BeautifulSoup, chapter_num: int) -> str:
        """Extract chapter title from HTML content."""
        # Try different heading tags
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            heading = soup.find(tag)
            if heading and heading.get_text().strip():
                return heading.get_text().strip()
        
        # Try title tag
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text().strip():
            return title_tag.get_text().strip()
        
        # Fallback to generic chapter name
        return f"Chapter {chapter_num}"
    
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract clean text content from HTML."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_cover_image(self, book: epub.EpubBook) -> Optional[bytes]:
        """Extract cover image from EPUB if available."""
        try:
            # Try to get cover image
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_COVER:
                    return item.get_content()
                
                # Check if it's marked as cover in properties
                if hasattr(item, 'properties') and 'cover-image' in item.properties:
                    return item.get_content()
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not extract cover image: {str(e)}")
            return None
    
    def get_book_info(self, epub_path: str) -> Dict[str, Any]:
        """Get basic information about an EPUB file without full parsing."""
        try:
            book = epub.read_epub(epub_path)
            metadata = self._extract_metadata(book)
            
            # Count chapters quickly
            spine_items = [item[0] for item in book.spine if item[1] == 'yes']
            chapter_count = len(spine_items)
            
            return {
                'title': metadata.get('title', 'Unknown'),
                'author': metadata.get('author', 'Unknown'),
                'language': metadata.get('language', 'en'),
                'chapter_count': chapter_count,
                'file_size': os.path.getsize(epub_path)
            }
            
        except Exception as e:
            logger.error(f"Error getting book info: {str(e)}")
            return {}

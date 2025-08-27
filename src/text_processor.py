"""
Text Processor Module

Handles text cleaning, processing, and preparation for TTS conversion.
"""

import re
import logging
from typing import List, Dict, Optional
import unicodedata

logger = logging.getLogger(__name__)

class TextProcessor:
    """
    Processes and cleans text content for optimal TTS conversion.
    """
    
    def __init__(self):
        # Common abbreviations and their expansions
        self.abbreviations = {
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Missus',
            'Ms.': 'Miss',
            'Prof.': 'Professor',
            'St.': 'Saint',
            'Ltd.': 'Limited',
            'Inc.': 'Incorporated',
            'Corp.': 'Corporation',
            'Co.': 'Company',
            'etc.': 'etcetera',
            'vs.': 'versus',
            'e.g.': 'for example',
            'i.e.': 'that is',
            'cf.': 'compare',
            'et al.': 'and others',
            'Ph.D.': 'Doctor of Philosophy',
            'M.D.': 'Doctor of Medicine',
            'B.A.': 'Bachelor of Arts',
            'M.A.': 'Master of Arts',
            'B.S.': 'Bachelor of Science',
            'M.S.': 'Master of Science',
            'U.S.': 'United States',
            'U.K.': 'United Kingdom',
            'U.N.': 'United Nations',
            'USA': 'United States of America',
            'UK': 'United Kingdom',
            'EU': 'European Union',
            'NATO': 'North Atlantic Treaty Organization',
            'CEO': 'Chief Executive Officer',
            'CFO': 'Chief Financial Officer',
            'CTO': 'Chief Technology Officer',
            'HR': 'Human Resources',
            'IT': 'Information Technology',
            'AI': 'Artificial Intelligence',
            'API': 'Application Programming Interface',
            'URL': 'Uniform Resource Locator',
            'HTTP': 'Hypertext Transfer Protocol',
            'HTML': 'Hypertext Markup Language',
            'CSS': 'Cascading Style Sheets',
            'JS': 'JavaScript',
            'SQL': 'Structured Query Language',
            'XML': 'Extensible Markup Language',
            'JSON': 'JavaScript Object Notation',
            'PDF': 'Portable Document Format',
            'GPS': 'Global Positioning System',
            'DVD': 'Digital Versatile Disc',
            'CD': 'Compact Disc',
            'TV': 'Television',
            'PC': 'Personal Computer',
            'FAQ': 'Frequently Asked Questions',
            'ATM': 'Automated Teller Machine',
            'GPS': 'Global Positioning System',
            'WiFi': 'Wireless Fidelity',
            'USB': 'Universal Serial Bus',
            'RAM': 'Random Access Memory',
            'CPU': 'Central Processing Unit',
            'GPU': 'Graphics Processing Unit',
            'SSD': 'Solid State Drive',
            'HDD': 'Hard Disk Drive'
        }
        
        # Patterns for text cleaning
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        self.number_pattern = re.compile(r'\b\d+\b')
        
        # Sentence ending patterns
        self.sentence_endings = re.compile(r'[.!?]+')
        
        # Multiple whitespace pattern
        self.whitespace_pattern = re.compile(r'\s+')
        
        # Dialogue patterns
        self.dialogue_pattern = re.compile(r'"([^"]*)"')
        
    def clean_text(self, text: str) -> str:
        """
        Clean and process text for optimal TTS conversion.
        
        Args:
            text (str): Raw text content
            
        Returns:
            str: Cleaned and processed text
        """
        if not text or not isinstance(text, str):
            return ""
        
        try:
            # Remove or replace problematic characters
            text = self._normalize_unicode(text)
            
            # Remove unwanted content
            text = self._remove_unwanted_content(text)
            
            # Expand abbreviations
            text = self._expand_abbreviations(text)
            
            # Clean numbers and special characters
            text = self._process_numbers(text)
            
            # Process dialogue and quotes
            text = self._process_dialogue(text)
            
            # Clean whitespace and formatting
            text = self._clean_formatting(text)
            
            # Ensure proper sentence structure
            text = self._fix_sentence_structure(text)
            
            logger.debug(f"Cleaned text: {len(text)} characters")
            return text
            
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            return text  # Return original text if cleaning fails
    
    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters."""
        # Normalize unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Replace smart quotes and dashes
        replacements = {
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '–': '-',
            '—': ' - ',
            '…': '...',
            '«': '"',
            '»': '"',
            '‹': "'",
            '›': "'",
            '‚': ',',
            '„': '"',
            '‟': '"',
            '′': "'",
            '″': '"',
            '‴': '"""',
            '‼': '!!',
            '⁇': '??',
            '⁈': '?!',
            '⁉': '!?'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def _remove_unwanted_content(self, text: str) -> str:
        """Remove unwanted content like URLs, emails, etc."""
        # Remove URLs
        text = self.url_pattern.sub('', text)
        
        # Remove email addresses
        text = self.email_pattern.sub('', text)
        
        # Remove phone numbers (optional - might be part of content)
        # text = self.phone_pattern.sub('', text)
        
        # Remove HTML tags if any remain
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[!]{3,}', '!', text)
        text = re.sub(r'[?]{3,}', '?', text)
        text = re.sub(r'[.]{4,}', '...', text)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common abbreviations."""
        # Sort by length (longest first) to avoid partial replacements
        sorted_abbrevs = sorted(self.abbreviations.items(), key=lambda x: len(x[0]), reverse=True)
        
        for abbrev, expansion in sorted_abbrevs:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _process_numbers(self, text: str) -> str:
        """Process numbers for better TTS pronunciation."""
        def number_to_words(match):
            num = match.group()
            try:
                # For very large numbers, keep as digits
                if len(num) > 10:
                    return num
                
                # Convert common numbers to words
                number_words = {
                    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
                    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
                    '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen',
                    '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen',
                    '18': 'eighteen', '19': 'nineteen', '20': 'twenty'
                }
                
                if num in number_words:
                    return number_words[num]
                
                # For other numbers, return as is for now
                return num
                
            except:
                return num
        
        # Convert standalone single-digit numbers
        text = re.sub(r'\b[0-9]\b', number_to_words, text)
        
        return text
    
    def _process_dialogue(self, text: str) -> str:
        """Process dialogue and quoted text."""
        # Add slight pauses before and after dialogue
        def process_quote(match):
            quoted_text = match.group(1)
            return f', "{quoted_text}", '
        
        text = self.dialogue_pattern.sub(process_quote, text)
        
        return text
    
    def _clean_formatting(self, text: str) -> str:
        """Clean formatting and whitespace."""
        # Remove excessive whitespace
        text = self.whitespace_pattern.sub(' ', text)
        
        # Remove leading and trailing whitespace
        text = text.strip()
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.!?,:;])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text
    
    def _fix_sentence_structure(self, text: str) -> str:
        """Fix sentence structure for better TTS flow."""
        # Ensure sentences end with proper punctuation
        sentences = self.sentence_endings.split(text)
        
        processed_sentences = []
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence:
                # Add period if sentence doesn't end with punctuation
                if not re.search(r'[.!?]$', sentence):
                    sentence += '.'
                processed_sentences.append(sentence)
        
        # Join sentences with proper spacing
        text = ' '.join(processed_sentences)
        
        return text
    
    def split_into_chunks(self, text: str, max_length: int = 500) -> List[str]:
        """
        Split text into chunks for TTS processing.
        
        Args:
            text (str): Text to split
            max_length (int): Maximum length per chunk
            
        Returns:
            List[str]: List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def estimate_reading_time(self, text: str, wpm: int = 150) -> float:
        """
        Estimate reading time in minutes.
        
        Args:
            text (str): Text content
            wpm (int): Words per minute reading speed
            
        Returns:
            float: Estimated reading time in minutes
        """
        word_count = len(text.split())
        return word_count / wpm
    
    def get_text_statistics(self, text: str) -> Dict[str, int]:
        """Get basic text statistics."""
        return {
            'characters': len(text),
            'words': len(text.split()),
            'sentences': len(re.split(r'[.!?]+', text)),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
        }
    
    def _create_safe_filename(self, title: str) -> str:
        """Create a safe filename from chapter title."""
        # Remove invalid characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
        safe_title = ''.join(c for c in title if c in safe_chars)
        
        # Replace spaces with underscores and limit length
        safe_title = safe_title.replace(' ', '_')[:50]
        
        # Remove leading/trailing dots and dashes
        safe_title = safe_title.strip('.-_')
        
        return safe_title or "chapter"

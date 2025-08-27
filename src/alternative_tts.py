"""
Alternative TTS Engine for Python 3.13 Compatibility

This is a fallback TTS engine that works when Coqui-TTS is not available.
It uses pyttsx3 which works with Python 3.13.
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

logger = logging.getLogger(__name__)

class AlternativeTTSEngine:
    """
    Fallback TTS engine using pyttsx3 for Python 3.13 compatibility.
    Lower quality than Coqui-TTS but functional for testing.
    """
    
    def __init__(self, config: Dict[str, Any]):
        if not PYTTSX3_AVAILABLE:
            raise ImportError("pyttsx3 is not available. Install with: pip install pyttsx3")
        
        self.config = config
        
        # Initialize pyttsx3 engine with error handling
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3 engine: {e}")
            raise ImportError(f"pyttsx3 initialization failed: {e}")
        
        # Configure voice settings
        self.speed = config.get('speed', 1.0)
        self.pitch = config.get('pitch', 1.0)
        
        try:
            # Set speech rate
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', int(rate * self.speed))
            
            # Try to set voice
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > 0:
                # Use first available voice, or try to find English voice
                selected_voice = voices[0]
                for voice in voices:
                    if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                        selected_voice = voice
                        break
                self.engine.setProperty('voice', selected_voice.id)
                logger.info(f"Using voice: {selected_voice.name}")
        except Exception as e:
            logger.warning(f"Could not configure voice settings: {e}")
        
        logger.info("Alternative TTS Engine initialized (pyttsx3)")
        logger.warning("Using fallback TTS engine. Quality may be lower than Coqui-TTS.")
    
    def text_to_speech(self, text: str, chapter_title: str, output_dir: str, 
                      chapter_num: int) -> Optional[str]:
        """
        Convert text to speech and save as audio file.
        """
        try:
            if not text.strip():
                logger.warning(f"Empty text for chapter {chapter_num}")
                return None
            
            # Create safe filename
            safe_title = self._create_safe_filename(chapter_title)
            output_filename = f"chapter_{chapter_num:03d}_{safe_title}.wav"
            output_path = os.path.join(output_dir, output_filename)
            
            logger.info(f"Generating audio for chapter {chapter_num}: {chapter_title}")
            
            # Save to file
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024  # KB
                logger.info(f"Generated audio file: {output_path} ({file_size:.1f} KB)")
                return output_path
            else:
                logger.error(f"Failed to generate audio file: {output_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating audio for chapter {chapter_num}: {str(e)}")
            return None
    
    def _create_safe_filename(self, title: str) -> str:
        """Create a safe filename from chapter title."""
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
        safe_title = ''.join(c for c in title if c in safe_chars)
        safe_title = safe_title.replace(' ', '_')[:50]
        safe_title = safe_title.strip('.-_')
        return safe_title or "chapter"
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices."""
        try:
            voices = self.engine.getProperty('voices')
            return [voice.name for voice in voices] if voices else ['default']
        except:
            return ['default']
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return ['en']  # pyttsx3 typically supports system default language
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if hasattr(self, 'engine'):
                del self.engine
            logger.info("Alternative TTS engine cleaned up")
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")

def check_pyttsx3_available():
    """Check if pyttsx3 is available without installing."""
    return PYTTSX3_AVAILABLE

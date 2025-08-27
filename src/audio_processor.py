"""
Audio Processor Module

Handles audio file processing, merging, and metadata management.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile
import datetime

from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, APIC, CHAP, CTOC
from mutagen.mp3 import MP3
import mutagen

logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Processes audio files, merges chapters, and adds metadata.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_format = config.get('output_format', 'm4b').lower()
        self.chapter_pause = config.get('chapter_pause', 2.0) * 1000  # Convert to ms
        self.quality = config.get('audio_quality', 'high')
        
        # Audio format settings
        self.format_settings = {
            'mp3': {
                'format': 'mp3',
                'parameters': {
                    'bitrate': '128k' if self.quality == 'standard' else '192k',
                    'codec': 'mp3'
                }
            },
            'm4b': {
                'format': 'mp4',
                'parameters': {
                    'bitrate': '64k' if self.quality == 'standard' else '128k',
                    'codec': 'aac'
                }
            }
        }
        
        logger.info(f"Audio processor initialized for {self.output_format} format")
    
    def merge_audiobook(self, audio_files: List[Dict[str, Any]], 
                       book_data: Dict[str, Any], output_dir: str) -> Optional[str]:
        """
        Merge individual chapter audio files into a complete audiobook.
        
        Args:
            audio_files (List[Dict]): List of audio file information
            book_data (Dict): Book metadata and information
            output_dir (str): Output directory for final audiobook
            
        Returns:
            str: Path to final audiobook file or None if failed
        """
        try:
            logger.info("Starting audiobook merge process...")
            
            # Create output filename
            output_filename = self._create_output_filename(book_data)
            output_path = os.path.join(output_dir, output_filename)
            
            # Sort audio files by chapter number
            sorted_files = sorted(audio_files, key=lambda x: x['chapter_num'])
            
            # Merge audio files
            logger.info(f"Merging {len(sorted_files)} audio files...")
            merged_audio = self._merge_audio_files(sorted_files)
            
            if not merged_audio:
                logger.error("Failed to merge audio files")
                return None
            
            # Export in the specified format
            temp_path = self._export_audio(merged_audio, output_path)
            
            if not temp_path:
                logger.error("Failed to export merged audio")
                return None
            
            # Add metadata and chapters
            final_path = self._add_metadata_and_chapters(
                temp_path, output_path, book_data, sorted_files
            )
            
            # Clean up temporary file if different from final
            if temp_path != final_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            
            if final_path and os.path.exists(final_path):
                file_size = os.path.getsize(final_path) / (1024 * 1024)  # MB
                logger.info(f"Audiobook created successfully: {final_path} ({file_size:.2f} MB)")
                return final_path
            else:
                logger.error("Failed to create final audiobook file")
                return None
                
        except Exception as e:
            logger.error(f"Error merging audiobook: {str(e)}")
            return None
    
    def _merge_audio_files(self, audio_files: List[Dict[str, Any]]) -> Optional[AudioSegment]:
        """Merge individual audio files with chapter pauses."""
        try:
            if not audio_files:
                return None
            
            # Load first audio file
            first_file = audio_files[0]['file']
            if not os.path.exists(first_file):
                logger.error(f"Audio file not found: {first_file}")
                return None
            
            combined_audio = AudioSegment.from_wav(first_file)
            logger.debug(f"Loaded first file: {first_file}")
            
            # Create chapter pause
            pause = AudioSegment.silent(duration=int(self.chapter_pause))
            
            # Merge remaining files
            for i, audio_info in enumerate(audio_files[1:], 1):
                audio_file = audio_info['file']
                
                if not os.path.exists(audio_file):
                    logger.warning(f"Audio file not found, skipping: {audio_file}")
                    continue
                
                try:
                    chapter_audio = AudioSegment.from_wav(audio_file)
                    combined_audio += pause + chapter_audio
                    logger.debug(f"Merged file {i+1}/{len(audio_files)}: {audio_file}")
                except Exception as e:
                    logger.warning(f"Error loading audio file {audio_file}: {str(e)}")
                    continue
            
            logger.info(f"Merged audio duration: {len(combined_audio) / 1000:.1f} seconds")
            return combined_audio
            
        except Exception as e:
            logger.error(f"Error merging audio files: {str(e)}")
            return None
    
    def _export_audio(self, audio: AudioSegment, output_path: str) -> Optional[str]:
        """Export audio in the specified format."""
        try:
            format_info = self.format_settings[self.output_format]
            
            # For M4B, we export as MP4 first
            if self.output_format == 'm4b':
                temp_path = output_path.replace('.m4b', '.mp4')
                audio.export(
                    temp_path,
                    format=format_info['format'],
                    bitrate=format_info['parameters']['bitrate'],
                    codec=format_info['parameters']['codec']
                )
                return temp_path
            else:
                # Direct export for MP3
                audio.export(
                    output_path,
                    format=format_info['format'],
                    bitrate=format_info['parameters']['bitrate']
                )
                return output_path
                
        except Exception as e:
            logger.error(f"Error exporting audio: {str(e)}")
            return None
    
    def _add_metadata_and_chapters(self, temp_path: str, final_path: str, 
                                  book_data: Dict[str, Any], 
                                  audio_files: List[Dict[str, Any]]) -> Optional[str]:
        """Add metadata and chapter information to the audiobook."""
        try:
            metadata = book_data['metadata']
            
            if self.output_format == 'm4b':
                return self._add_m4b_metadata(temp_path, final_path, metadata, audio_files)
            else:
                return self._add_mp3_metadata(temp_path, metadata, audio_files)
                
        except Exception as e:
            logger.error(f"Error adding metadata: {str(e)}")
            return temp_path  # Return original file if metadata fails
    
    def _add_m4b_metadata(self, temp_path: str, final_path: str, 
                         metadata: Dict[str, str], 
                         audio_files: List[Dict[str, Any]]) -> Optional[str]:
        """Add metadata and chapters to M4B file."""
        try:
            # Rename temp file to final M4B extension
            os.rename(temp_path, final_path)
            
            # Load M4B file
            audiobook = MP4(final_path)
            
            # Add basic metadata
            audiobook['\xa9nam'] = metadata.get('title', 'Unknown Title')
            audiobook['\xa9ART'] = metadata.get('author', 'Unknown Author')
            audiobook['\xa9alb'] = metadata.get('title', 'Unknown Title')
            audiobook['\xa9day'] = metadata.get('date', str(datetime.datetime.now().year))
            audiobook['\xa9gen'] = 'Audiobook'
            audiobook['stik'] = [2]  # Audiobook type
            
            if metadata.get('description'):
                audiobook['desc'] = metadata['description']
            
            # Add chapter markers
            self._add_m4b_chapters(audiobook, audio_files)
            
            # Save metadata
            audiobook.save()
            
            logger.info("M4B metadata and chapters added successfully")
            return final_path
            
        except Exception as e:
            logger.error(f"Error adding M4B metadata: {str(e)}")
            return final_path
    
    def _add_m4b_chapters(self, audiobook: MP4, audio_files: List[Dict[str, Any]]):
        """Add chapter markers to M4B file."""
        try:
            # Calculate chapter start times
            current_time = 0
            chapters = []
            
            for audio_info in audio_files:
                audio_file = audio_info['file']
                if os.path.exists(audio_file):
                    # Get duration of audio file
                    audio = AudioSegment.from_wav(audio_file)
                    duration = len(audio)  # in milliseconds
                    
                    chapters.append({
                        'title': audio_info['title'],
                        'start_time': current_time,
                        'duration': duration
                    })
                    
                    current_time += duration + self.chapter_pause
            
            # Add chapter metadata (simplified - full implementation would need more complex chapter handling)
            if chapters:
                chapter_list = []
                for i, chapter in enumerate(chapters):
                    chapter_list.append(f"Chapter {i+1}: {chapter['title']}")
                
                # Store chapter information as description or comment
                audiobook['©cmt'] = '; '.join(chapter_list)
            
        except Exception as e:
            logger.warning(f"Could not add detailed chapters: {str(e)}")
    
    def _add_mp3_metadata(self, file_path: str, metadata: Dict[str, str], 
                         audio_files: List[Dict[str, Any]]) -> str:
        """Add metadata to MP3 file."""
        try:
            # Load MP3 file
            audiobook = MP3(file_path, ID3=ID3)
            
            # Add ID3 tags if they don't exist
            try:
                audiobook.add_tags()
            except mutagen.id3.error:
                pass  # Tags already exist
            
            # Add basic metadata
            audiobook.tags.add(TIT2(encoding=3, text=metadata.get('title', 'Unknown Title')))
            audiobook.tags.add(TPE1(encoding=3, text=metadata.get('author', 'Unknown Author')))
            audiobook.tags.add(TALB(encoding=3, text=metadata.get('title', 'Unknown Title')))
            audiobook.tags.add(TDRC(encoding=3, text=metadata.get('date', str(datetime.datetime.now().year))))
            audiobook.tags.add(TCON(encoding=3, text='Audiobook'))
            
            # Save metadata
            audiobook.save()
            
            logger.info("MP3 metadata added successfully")
            return file_path
            
        except Exception as e:
            logger.error(f"Error adding MP3 metadata: {str(e)}")
            return file_path
    
    def _create_output_filename(self, book_data: Dict[str, Any]) -> str:
        """Create a safe output filename for the audiobook."""
        metadata = book_data['metadata']
        title = metadata.get('title', 'Unknown_Title')
        author = metadata.get('author', 'Unknown_Author')
        
        # Create safe filename
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. "
        safe_title = ''.join(c for c in title if c in safe_chars).replace(' ', '_')
        safe_author = ''.join(c for c in author if c in safe_chars).replace(' ', '_')
        
        # Limit length
        safe_title = safe_title[:50]
        safe_author = safe_author[:30]
        
        # Create filename
        filename = f"{safe_author}-{safe_title}.{self.output_format}"
        
        return filename
    
    def get_audio_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about an audio file."""
        try:
            audio = AudioSegment.from_file(file_path)
            
            return {
                'duration_seconds': len(audio) / 1000,
                'duration_formatted': self._format_duration(len(audio) / 1000),
                'sample_rate': audio.frame_rate,
                'channels': audio.channels,
                'file_size_mb': os.path.getsize(file_path) / (1024 * 1024)
            }
            
        except Exception as e:
            logger.error(f"Error getting audio info: {str(e)}")
            return {}
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def cleanup_temp_files(self, temp_files: List[str]):
        """Clean up temporary audio files."""
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.debug(f"Removed temporary file: {file_path}")
            except Exception as e:
                logger.warning(f"Could not remove temporary file {file_path}: {str(e)}")
    
    def validate_audio_file(self, file_path: str) -> bool:
        """Validate if an audio file is readable."""
        try:
            AudioSegment.from_file(file_path)
            return True
        except Exception:
            return False

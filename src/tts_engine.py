"""
Text-to-Speech Engine Module

Handles text-to-speech conversion using various TTS engines with GPU acceleration support.
"""

import os
import logging
import tempfile
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
import time

import torch
import numpy as np
from TTS.api import TTS
import soundfile as sf

logger = logging.getLogger(__name__)

class TTSEngine:
    """
    High-quality text-to-speech engine with GPU acceleration support.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = self._setup_device()
        self.tts_model = None
        self.model_name = config.get('tts_model', 'tts_models/en/ljspeech/tacotron2-DDC')
        self.voice = config.get('voice', 'en')
        self.speaker = config.get('speaker', 'default')
        self.speed = config.get('speed', 1.0)
        self.pitch = config.get('pitch', 1.0)
        
        # Initialize TTS model
        self._initialize_tts()
        
        logger.info(f"TTS Engine initialized with device: {self.device}")
    
    def _setup_device(self) -> str:
        """Setup computation device (CPU/GPU)."""
        if self.config.get('gpu_acceleration', False) and torch.cuda.is_available():
            device = 'cuda'
            logger.info(f"GPU acceleration enabled: {torch.cuda.get_device_name()}")
        else:
            device = 'cpu'
            logger.info("Using CPU for TTS processing")
        
        return device
    
    def _initialize_tts(self):
        """Initialize the TTS model."""
        try:
            # Determine the best model based on language
            model_name = self._get_model_for_language(self.voice)
            
            logger.info(f"Loading TTS model: {model_name}")
            
            # Initialize TTS with the selected model
            self.tts_model = TTS(model_name=model_name, progress_bar=False, gpu=self.device == 'cuda')
            
            # Check if model supports multiple speakers
            if hasattr(self.tts_model, 'speakers') and self.tts_model.speakers:
                logger.info(f"Available speakers: {self.tts_model.speakers[:5]}...")  # Show first 5
                
                # Select speaker if specified
                if self.speaker != 'default' and self.speaker in self.tts_model.speakers:
                    logger.info(f"Using speaker: {self.speaker}")
                elif self.tts_model.speakers:
                    self.speaker = self.tts_model.speakers[0]
                    logger.info(f"Using default speaker: {self.speaker}")
            
            logger.info("TTS model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error initializing TTS model: {str(e)}")
            # Fallback to default model
            try:
                logger.info("Falling back to default TTS model")
                self.tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", 
                                   progress_bar=False, 
                                   gpu=self.device == 'cuda')
            except Exception as fallback_error:
                logger.error(f"Failed to load fallback model: {str(fallback_error)}")
                raise
    
    def _get_model_for_language(self, language: str) -> str:
        """Get the best TTS model for the specified language."""
        language_models = {
            'en': 'tts_models/en/ljspeech/tacotron2-DDC',
            'es': 'tts_models/es/mai/tacotron2-DDC',
            'fr': 'tts_models/fr/mai/tacotron2-DDC',
            'de': 'tts_models/de/mai/tacotron2-DDC',
            'it': 'tts_models/it/mai/tacotron2-DDC',
            'pt': 'tts_models/pt/cv/vits',
            'ru': 'tts_models/ru/cv/vits',
            'zh': 'tts_models/zh-CN/baker/tacotron2-DDC',
            'ja': 'tts_models/ja/kokoro/tacotron2-DDC',
            'ko': 'tts_models/ko/kss/vits',
            'ar': 'tts_models/ar/cv/vits',
            'hi': 'tts_models/hi/cv/vits',
        }
        
        return language_models.get(language.lower(), 'tts_models/en/ljspeech/tacotron2-DDC')
    
    def text_to_speech(self, text: str, chapter_title: str, output_dir: str, 
                      chapter_num: int) -> Optional[str]:
        """
        Convert text to speech and save as audio file.
        
        Args:
            text (str): Text content to convert
            chapter_title (str): Chapter title for filename
            output_dir (str): Output directory
            chapter_num (int): Chapter number
            
        Returns:
            str: Path to generated audio file or None if failed
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
            
            # Split text into chunks if too long
            text_chunks = self._split_text_for_tts(text)
            
            if len(text_chunks) == 1:
                # Single chunk - direct conversion
                self._generate_audio_chunk(text_chunks[0], output_path)
            else:
                # Multiple chunks - generate and merge
                chunk_files = []
                temp_dir = tempfile.mkdtemp()
                
                try:
                    for i, chunk in enumerate(text_chunks):
                        chunk_path = os.path.join(temp_dir, f"chunk_{i:03d}.wav")
                        self._generate_audio_chunk(chunk, chunk_path)
                        chunk_files.append(chunk_path)
                    
                    # Merge chunks
                    self._merge_audio_chunks(chunk_files, output_path)
                    
                finally:
                    # Clean up temporary files
                    for file in chunk_files:
                        try:
                            os.remove(file)
                        except:
                            pass
                    try:
                        os.rmdir(temp_dir)
                    except:
                        pass
            
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
    
    def _generate_audio_chunk(self, text: str, output_path: str):
        """Generate audio for a single text chunk."""
        try:
            # Generate audio
            if hasattr(self.tts_model, 'speakers') and self.tts_model.speakers and self.speaker != 'default':
                # Model supports speakers
                wav = self.tts_model.tts(text=text, speaker=self.speaker)
            else:
                # Standard TTS
                wav = self.tts_model.tts(text=text)
            
            # Convert to numpy array if needed
            if isinstance(wav, list):
                wav = np.array(wav)
            
            # Apply speed and pitch modifications
            wav = self._apply_audio_effects(wav)
            
            # Save audio file
            sf.write(output_path, wav, self.tts_model.synthesizer.output_sample_rate)
            
        except Exception as e:
            logger.error(f"Error generating audio chunk: {str(e)}")
            raise
    
    def _apply_audio_effects(self, wav: np.ndarray) -> np.ndarray:
        """Apply speed and pitch effects to audio."""
        try:
            # Apply speed change
            if self.speed != 1.0:
                # Simple speed change by resampling
                import librosa
                wav = librosa.effects.time_stretch(wav, rate=1.0/self.speed)
            
            # Apply pitch change
            if self.pitch != 1.0:
                # Simple pitch shift
                import librosa
                n_steps = 12 * np.log2(self.pitch)  # Convert to semitones
                wav = librosa.effects.pitch_shift(wav, sr=self.tts_model.synthesizer.output_sample_rate, 
                                                n_steps=n_steps)
            
            return wav
            
        except Exception as e:
            logger.warning(f"Could not apply audio effects: {str(e)}")
            return wav  # Return unmodified audio
    
    def _split_text_for_tts(self, text: str, max_length: int = 500) -> List[str]:
        """Split text into chunks suitable for TTS processing."""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = text.split('. ')
        
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_length:  # +2 for '. '
                if current_chunk:
                    current_chunk += ". " + sentence
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk + ".")
                current_chunk = sentence
        
        if current_chunk:
            if not current_chunk.endswith('.'):
                current_chunk += "."
            chunks.append(current_chunk)
        
        return chunks
    
    def _merge_audio_chunks(self, chunk_files: List[str], output_path: str):
        """Merge multiple audio chunks into a single file."""
        try:
            from pydub import AudioSegment
            
            # Load first chunk
            combined = AudioSegment.from_wav(chunk_files[0])
            
            # Add small pause between chunks
            pause = AudioSegment.silent(duration=300)  # 300ms pause
            
            # Merge remaining chunks
            for chunk_file in chunk_files[1:]:
                chunk = AudioSegment.from_wav(chunk_file)
                combined += pause + chunk
            
            # Export as WAV
            combined.export(output_path, format="wav")
            
        except Exception as e:
            logger.error(f"Error merging audio chunks: {str(e)}")
            raise
    
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
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices/speakers."""
        try:
            if hasattr(self.tts_model, 'speakers') and self.tts_model.speakers:
                return list(self.tts_model.speakers)
            else:
                return ['default']
        except:
            return ['default']
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi']
    
    def estimate_generation_time(self, text: str) -> float:
        """Estimate time needed to generate audio (in seconds)."""
        # Rough estimation: 1 second per 10 words for CPU, 1 second per 30 words for GPU
        word_count = len(text.split())
        if self.device == 'cuda':
            return word_count / 30.0
        else:
            return word_count / 10.0
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if self.tts_model:
                del self.tts_model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info("TTS engine cleaned up")
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup()

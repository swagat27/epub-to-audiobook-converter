"""
Configuration Manager Module

Handles application configuration and settings management.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Manages application configuration from files and environment variables.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config = self._load_default_config()
        
        # Load configuration from file if provided
        if config_file:
            self._load_config_file(config_file)
        
        # Override with environment variables
        self._load_env_config()
        
        logger.info("Configuration loaded successfully")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration settings."""
        return {
            # TTS Settings
            'tts_model': 'tts_models/en/ljspeech/tacotron2-DDC',
            'voice': 'en',
            'speaker': 'default',
            'speed': 1.0,
            'pitch': 1.0,
            'gpu_acceleration': False,
            
            # Audio Settings
            'output_format': 'm4b',
            'audio_quality': 'high',  # 'standard' or 'high'
            'chapter_pause': 2.0,  # seconds
            'max_chunk_length': 500,  # characters
            
            # Processing Settings
            'max_workers': 2,
            'temp_dir': './temp',
            'cleanup_temp': True,
            
            # Text Processing
            'text_normalization': True,
            'expand_abbreviations': True,
            'remove_urls': True,
            'remove_emails': True,
            
            # Output Settings
            'output_dir': './output',
            'preserve_structure': True,
            'add_metadata': True,
            'add_chapters': True,
            
            # Logging
            'log_level': 'INFO',
            'log_file': './logs/app.log',
            'console_logging': True,
            
            # Advanced Settings
            'retry_attempts': 3,
            'retry_delay': 1.0,
            'progress_updates': True,
            'memory_limit': '2GB',
            
            # Language-specific settings
            'language_models': {
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
                'hi': 'tts_models/hi/cv/vits'
            },
            
            # Performance tuning
            'batch_size': 1,
            'torch_threads': None,  # Auto-detect
            'gpu_memory_fraction': 0.8,
            
            # Quality settings
            'sample_rate': 22050,
            'audio_bitrate': {
                'standard': {'mp3': '128k', 'm4b': '64k'},
                'high': {'mp3': '192k', 'm4b': '128k'}
            },
            
            # Feature flags
            'enable_noise_reduction': False,
            'enable_audio_normalization': True,
            'enable_silence_detection': True,
            'enable_progress_bar': True
        }
    
    def _load_config_file(self, config_file: str):
        """Load configuration from JSON file."""
        try:
            if not os.path.exists(config_file):
                logger.warning(f"Config file not found: {config_file}")
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
            
            # Merge with default config
            self.config.update(file_config)
            logger.info(f"Configuration loaded from: {config_file}")
            
        except Exception as e:
            logger.error(f"Error loading config file: {str(e)}")
    
    def _load_env_config(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'EPUB_TTS_MODEL': 'tts_model',
            'EPUB_VOICE': 'voice',
            'EPUB_SPEAKER': 'speaker',
            'EPUB_SPEED': ('speed', float),
            'EPUB_PITCH': ('pitch', float),
            'EPUB_GPU': ('gpu_acceleration', self._str_to_bool),
            'EPUB_FORMAT': 'output_format',
            'EPUB_QUALITY': 'audio_quality',
            'EPUB_PAUSE': ('chapter_pause', float),
            'EPUB_OUTPUT_DIR': 'output_dir',
            'EPUB_LOG_LEVEL': 'log_level',
            'EPUB_MAX_WORKERS': ('max_workers', int),
            'EPUB_CLEANUP': ('cleanup_temp', self._str_to_bool),
            'EPUB_TORCH_THREADS': ('torch_threads', int),
            'EPUB_MEMORY_LIMIT': 'memory_limit',
            'EPUB_BATCH_SIZE': ('batch_size', int),
            'EPUB_SAMPLE_RATE': ('sample_rate', int),
            'EPUB_GPU_MEMORY': ('gpu_memory_fraction', float)
        }
        
        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    if isinstance(config_key, tuple):
                        key, converter = config_key
                        self.config[key] = converter(env_value)
                    else:
                        self.config[config_key] = env_value
                    
                    logger.debug(f"Environment override: {env_var} = {env_value}")
                    
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid environment value for {env_var}: {env_value} ({str(e)})")
    
    def _str_to_bool(self, value: str) -> bool:
        """Convert string to boolean."""
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
    
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration dictionary."""
        return self.config.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        self.config[key] = value
        logger.debug(f"Configuration updated: {key} = {value}")
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values."""
        self.config.update(updates)
        logger.debug(f"Configuration updated with {len(updates)} values")
    
    def save_config(self, output_file: str):
        """Save current configuration to a JSON file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving config file: {str(e)}")
    
    def validate_config(self) -> bool:
        """Validate the current configuration."""
        try:
            # Validate required settings
            required_keys = ['voice', 'output_format', 'output_dir']
            for key in required_keys:
                if key not in self.config:
                    logger.error(f"Required configuration key missing: {key}")
                    return False
            
            # Validate value ranges
            validations = [
                ('speed', lambda x: 0.1 <= x <= 3.0, "Speed must be between 0.1 and 3.0"),
                ('pitch', lambda x: 0.1 <= x <= 3.0, "Pitch must be between 0.1 and 3.0"),
                ('chapter_pause', lambda x: 0.0 <= x <= 10.0, "Chapter pause must be between 0.0 and 10.0"),
                ('max_workers', lambda x: 1 <= x <= 16, "Max workers must be between 1 and 16"),
                ('output_format', lambda x: x in ['mp3', 'm4b'], "Output format must be 'mp3' or 'm4b'"),
                ('audio_quality', lambda x: x in ['standard', 'high'], "Audio quality must be 'standard' or 'high'"),
                ('log_level', lambda x: x in ['DEBUG', 'INFO', 'WARNING', 'ERROR'], "Invalid log level")
            ]
            
            for key, validator, message in validations:
                if key in self.config:
                    if not validator(self.config[key]):
                        logger.error(f"Configuration validation failed: {message}")
                        return False
            
            # Validate paths
            output_dir = self.config.get('output_dir')
            if output_dir:
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    logger.error(f"Cannot create output directory: {output_dir} ({str(e)})")
                    return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Error validating configuration: {str(e)}")
            return False
    
    def get_model_for_language(self, language: str) -> str:
        """Get the TTS model for a specific language."""
        language_models = self.config.get('language_models', {})
        return language_models.get(language.lower(), self.config.get('tts_model'))
    
    def get_audio_bitrate(self, format_type: str) -> str:
        """Get audio bitrate for a specific format and quality."""
        quality = self.config.get('audio_quality', 'high')
        bitrates = self.config.get('audio_bitrate', {})
        
        if quality in bitrates and format_type in bitrates[quality]:
            return bitrates[quality][format_type]
        
        # Fallback defaults
        defaults = {
            'mp3': {'standard': '128k', 'high': '192k'},
            'm4b': {'standard': '64k', 'high': '128k'}
        }
        
        return defaults.get(format_type, {}).get(quality, '128k')
    
    def create_sample_config(self, output_file: str):
        """Create a sample configuration file with comments."""
        sample_config = {
            "_comment": "EPUB to Audiobook Converter Configuration",
            "_version": "1.0",
            
            "tts_settings": {
                "tts_model": "tts_models/en/ljspeech/tacotron2-DDC",
                "voice": "en",
                "speaker": "default",
                "speed": 1.0,
                "pitch": 1.0,
                "gpu_acceleration": False,
                "_comment": "TTS engine settings. Set gpu_acceleration to true if you have a CUDA-compatible GPU."
            },
            
            "audio_settings": {
                "output_format": "m4b",
                "audio_quality": "high",
                "chapter_pause": 2.0,
                "_comment": "Audio output settings. Format can be 'mp3' or 'm4b'. Quality can be 'standard' or 'high'."
            },
            
            "processing_settings": {
                "max_chunk_length": 500,
                "max_workers": 2,
                "cleanup_temp": True,
                "_comment": "Processing optimization settings."
            },
            
            "output_settings": {
                "output_dir": "./output",
                "add_metadata": True,
                "add_chapters": True,
                "_comment": "Output file settings."
            },
            
            "advanced_settings": {
                "retry_attempts": 3,
                "memory_limit": "2GB",
                "torch_threads": None,
                "_comment": "Advanced settings for fine-tuning performance."
            }
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sample_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Sample configuration created: {output_file}")
            
        except Exception as e:
            logger.error(f"Error creating sample config: {str(e)}")
    
    def __str__(self) -> str:
        """String representation of the configuration."""
        return json.dumps(self.config, indent=2, default=str)

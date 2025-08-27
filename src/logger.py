"""
Logging Module

Provides comprehensive logging functionality for the EPUB to Audiobook converter.
"""

import os
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import sys
from datetime import datetime

def setup_logger(name: str, log_level: str = "INFO", 
                log_file: Optional[str] = None, 
                console_output: bool = True) -> logging.Logger:
    """
    Set up a comprehensive logger with file and console handlers.
    
    Args:
        name (str): Logger name
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file (str, optional): Path to log file
        console_output (bool): Whether to output to console
        
    Returns:
        logging.Logger: Configured logger
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        try:
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            # Create rotating file handler (max 10MB, keep 5 backups)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)  # File gets all messages
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            # If file logging fails, just log to console
            logger.warning(f"Could not set up file logging: {str(e)}")
    
    return logger

def setup_application_logging(config: dict) -> logging.Logger:
    """
    Set up application-wide logging based on configuration.
    
    Args:
        config (dict): Application configuration
        
    Returns:
        logging.Logger: Main application logger
    """
    
    log_level = config.get('log_level', 'INFO')
    log_file = config.get('log_file', './logs/epub_to_audiobook.log')
    console_logging = config.get('console_logging', True)
    
    # Set up main logger
    main_logger = setup_logger(
        'epub_to_audiobook',
        log_level=log_level,
        log_file=log_file,
        console_output=console_logging
    )
    
    # Set up component loggers
    component_loggers = [
        'epub_to_audiobook.epub_parser',
        'epub_to_audiobook.text_processor',
        'epub_to_audiobook.tts_engine',
        'epub_to_audiobook.audio_processor',
        'epub_to_audiobook.config_manager'
    ]
    
    for logger_name in component_loggers:
        component_logger = setup_logger(
            logger_name,
            log_level=log_level,
            log_file=log_file,
            console_output=False  # Only main logger outputs to console
        )
    
    # Log application startup
    main_logger.info("="*60)
    main_logger.info("EPUB to Audiobook Converter - Application Started")
    main_logger.info(f"Log Level: {log_level}")
    main_logger.info(f"Log File: {log_file}")
    main_logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main_logger.info("="*60)
    
    return main_logger

class ProgressLogger:
    """
    Logger for tracking progress of long-running operations.
    """
    
    def __init__(self, logger: logging.Logger, total_items: int, 
                 operation_name: str = "Processing"):
        self.logger = logger
        self.total_items = total_items
        self.operation_name = operation_name
        self.current_item = 0
        self.start_time = datetime.now()
        
    def update(self, increment: int = 1, item_name: str = None):
        """Update progress and log if needed."""
        self.current_item += increment
        
        # Log every 10% or at specific milestones
        if (self.current_item % max(1, self.total_items // 10) == 0 or 
            self.current_item == self.total_items):
            
            progress_percent = (self.current_item / self.total_items) * 100
            elapsed_time = (datetime.now() - self.start_time).total_seconds()
            
            if self.current_item < self.total_items and elapsed_time > 0:
                estimated_total = elapsed_time * self.total_items / self.current_item
                remaining_time = estimated_total - elapsed_time
                
                self.logger.info(
                    f"{self.operation_name}: {self.current_item}/{self.total_items} "
                    f"({progress_percent:.1f}%) - ETA: {remaining_time:.0f}s"
                    f"{f' - {item_name}' if item_name else ''}"
                )
            else:
                self.logger.info(
                    f"{self.operation_name}: {self.current_item}/{self.total_items} "
                    f"({progress_percent:.1f}%) - Complete!"
                )
    
    def finish(self):
        """Log completion of the operation."""
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        self.logger.info(
            f"{self.operation_name} completed in {elapsed_time:.1f} seconds"
        )

class PerformanceLogger:
    """
    Logger for tracking performance metrics.
    """
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.start_times = {}
        
    def start_timer(self, operation: str):
        """Start timing an operation."""
        self.start_times[operation] = datetime.now()
        self.logger.debug(f"Started: {operation}")
        
    def end_timer(self, operation: str, log_level: str = "INFO"):
        """End timing an operation and log the duration."""
        if operation in self.start_times:
            duration = (datetime.now() - self.start_times[operation]).total_seconds()
            
            level = getattr(logging, log_level.upper(), logging.INFO)
            self.logger.log(level, f"Completed: {operation} in {duration:.2f} seconds")
            
            del self.start_times[operation]
            return duration
        else:
            self.logger.warning(f"No start time found for operation: {operation}")
            return None
    
    def log_memory_usage(self):
        """Log current memory usage if psutil is available."""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.logger.debug(f"Memory usage: {memory_mb:.1f} MB")
        except ImportError:
            pass  # psutil not available
        except Exception as e:
            self.logger.debug(f"Could not get memory usage: {str(e)}")

def log_system_info(logger: logging.Logger):
    """Log system information for debugging purposes."""
    try:
        import platform
        import torch
        
        logger.info("System Information:")
        logger.info(f"  Platform: {platform.platform()}")
        logger.info(f"  Python: {platform.python_version()}")
        logger.info(f"  PyTorch: {torch.__version__}")
        logger.info(f"  CUDA Available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            logger.info(f"  CUDA Device: {torch.cuda.get_device_name()}")
            logger.info(f"  CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        
        # Log CPU info
        try:
            import psutil
            logger.info(f"  CPU Cores: {psutil.cpu_count()}")
            logger.info(f"  RAM: {psutil.virtual_memory().total / 1024**3:.1f} GB")
        except ImportError:
            pass
            
    except Exception as e:
        logger.warning(f"Could not log system info: {str(e)}")

def create_error_report(logger: logging.Logger, error: Exception, 
                       context: dict = None):
    """Create a detailed error report."""
    import traceback
    
    logger.error("="*50)
    logger.error("ERROR REPORT")
    logger.error(f"Error Type: {type(error).__name__}")
    logger.error(f"Error Message: {str(error)}")
    
    if context:
        logger.error("Context:")
        for key, value in context.items():
            logger.error(f"  {key}: {value}")
    
    logger.error("Traceback:")
    for line in traceback.format_exc().split('\n'):
        if line.strip():
            logger.error(f"  {line}")
    
    logger.error("="*50)

class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for console output (optional, for enhanced readability).
    """
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to level name
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_colored_console_logging(logger: logging.Logger):
    """Set up colored console logging if supported."""
    try:
        # Check if we're in a terminal that supports colors
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
            # Find console handler and replace formatter
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                    colored_formatter = ColoredFormatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
                    handler.setFormatter(colored_formatter)
                    break
    except Exception:
        pass  # Fall back to standard formatting

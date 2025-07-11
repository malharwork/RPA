import logging
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = f"logs/rpa_poc_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    # Set specific log levels for external libraries
    logging.getLogger('PIL').setLevel(logging.WARNING)
    logging.getLogger('opencv').setLevel(logging.WARNING)

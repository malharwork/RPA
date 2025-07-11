import os
import logging
from datetime import datetime

class RequestTracker:
    """Tracks customer unblock requests"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.logs_folder = self.config.get('paths.logs_folder', 'logs')
        self.tracking_file = os.path.join(self.logs_folder, 'unblock_requests.txt')
    
    def log_request(self, request_id: str, customer_name: str, 
                   status: str, timestamp: str = None) -> bool:
        """Log unblock request to tracking file"""
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Ensure logs directory exists
            os.makedirs(self.logs_folder, exist_ok=True)
            
            # Create log entry
            log_entry = f"{timestamp} | {request_id} | {customer_name} | {status}\n"
            
            # Append to tracking file
            with open(self.tracking_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            self.logger.info(f"Request logged: {request_id} - {status}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging request: {str(e)}")
            return False    
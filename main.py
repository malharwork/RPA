import os
import sys
import logging
from datetime import datetime
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logging
from utils.config_manager import ConfigManager

def setup_directories():
    """Create required directory structure"""
    directories = [
        'data/input', 'data/processed', 'data/exceptions',
        'logs', 'reports', 'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main execution function"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=" * 60)
    print("🤖 RPA POC - Order Processing & Customer Unblock")
    print("   Python Alternative Implementation")
    print("=" * 60)
    
    setup_directories()
    
    # Load configuration
    config_manager = ConfigManager()
    
    logger.info("Starting RPA POC Application")
    
    while True:
        print("\nSelect Process:")
        print("1. Order Processing")
        print("2. Customer Unblock") 
        print("3. Exit")
        
        choice = input("\nEnter choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            logger.info("Starting Order Processing workflow")
            from order_processing.main_processor import OrderProcessor
            processor = OrderProcessor(config_manager)
            processor.run()
            
        elif choice == "2":
            logger.info("Starting Customer Unblock workflow")
            from customer_unblock.main_processor import CustomerUnblockProcessor
            processor = CustomerUnblockProcessor(config_manager)
            processor.run()
            
        elif choice == "3":
            print("👋 Goodbye!")
            logger.info("Application terminated by user")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    sys.exit(0)

if __name__ == "__main__":
    main()

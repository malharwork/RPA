import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages configuration settings for the RPA application"""
    
    def __init__(self, config_file='config/settings.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        default_config = {
            "email": {
                "smtp_server": "smtp.gmail.com",
                "port": 587,
                "sender_email": "your-email@gmail.com",
                "sender_password": "your-app-password",
                "management_emails": ["manager@company.com", "finance@company.com"]
            },
            "paths": {
                "input_folder": "data/input",
                "processed_folder": "data/processed", 
                "exceptions_folder": "data/exceptions",
                "reports_folder": "reports",
                "logs_folder": "logs",
                "sku_mapping_file": "config/sku_mapping.xlsx"
            },
            "processing": {
                "max_file_size_mb": 50,
                "supported_formats": [".txt", ".pdf", ".jpg", ".jpeg", ".png"],
                "ocr_language": "eng"
            }
        }
        
        # Create config directory and file
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        print(f"✅ Created default configuration file: {self.config_file}")
        print("📝 Please update email settings in the config file")
        
        return default_config
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def save(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
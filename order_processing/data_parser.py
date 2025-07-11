import re
import logging
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ParsedOrder:
    """Data class for parsed order information"""
    customer_name: str
    item_description: str
    quantity: str
    price: Optional[str] = None
    order_date: Optional[str] = None
    po_number: Optional[str] = None

class DataParser:
    """Parses text content to extract order information"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Regex patterns for data extraction
        self.patterns = {
            'customer': [
                r'(?i)(customer|client|company)[:\s]+([^\n\r]+)',
                r'(?i)(bill\s+to|sold\s+to)[:\s]+([^\n\r]+)',
                r'(?i)(from)[:\s]+([^\n\r]+)'
            ],
            'item': [
                r'(?i)(item|description|product)[:\s]+([^\n\r]+)',
                r'(?i)(part\s+description|item\s+description)[:\s]+([^\n\r]+)'
            ],
            'quantity': [
                r'(?i)(qty|quantity)[:\s]*(\d+)',
                r'(?i)(units?)[:\s]*(\d+)',
                r'(\d+)\s*(?i)(pcs|pieces|units?)'
            ],
            'price': [
                r'(?i)(price|amount|total)[:\s]*[\$]?(\d+\.?\d*)',
                r'[\$](\d+\.?\d*)'
            ],
            'po_number': [
                r'(?i)(po|purchase\s+order)[\s#]*(\w+)',
                r'(?i)(order\s+number)[:\s]*(\w+)'
            ],
            'date': [
                r'(?i)(date|order\s+date)[:\s]*([^\n\r]+)',
                r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
            ]
        }
    
    def parse_text(self, text: str) -> ParsedOrder:
        """Parse extracted text to find order details"""
        try:
            self.logger.info("Starting text parsing")
            
            # Extract information using patterns
            extracted_data = {}
            
            for field, patterns in self.patterns.items():
                extracted_data[field] = self._extract_field(text, patterns)
            
            # Create ParsedOrder object
            parsed_order = ParsedOrder(
                customer_name=extracted_data.get('customer', 'Unknown Customer'),
                item_description=extracted_data.get('item', 'Unknown Item'),
                quantity=extracted_data.get('quantity', '1'),
                price=extracted_data.get('price'),
                po_number=extracted_data.get('po_number'),
                order_date=extracted_data.get('date')
            )
            
            self.logger.info(f"Parsed order: {parsed_order}")
            return parsed_order
            
        except Exception as e:
            self.logger.error(f"Error parsing text: {str(e)}")
            raise
    
    def _extract_field(self, text: str, patterns: list) -> Optional[str]:
        """Extract field value using multiple patterns"""
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(-1).strip()
        return None
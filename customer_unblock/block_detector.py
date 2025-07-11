import logging
from typing import Optional, Tuple

class BlockDetector:
    """Simulates customer block detection in ERP system"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
    
    def detect_customer_block(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Detect blocked customer - simulated with user input"""
        self.logger.info("Starting customer block detection")
        
        print("\n🔍 Customer Block Detection Simulation")
        print("=" * 40)
        print("In a real system, this would monitor ERP for blocked customers.")
        print("For this POC, please simulate a customer block scenario.")
        print()
        
        response = input("Enter customer details (CustomerID|CustomerName|BlockReason) or 'NONE': ").strip()
        
        if response.upper() == 'NONE':
            print("✅ No customer blocks detected")
            return None, None, None
        
        try:
            parts = response.split('|')
            if len(parts) >= 3:
                customer_id = parts[0].strip()
                customer_name = parts[1].strip()
                block_reason = parts[2].strip()
                
                print(f"🚫 Customer block detected:")
                print(f"   ID: {customer_id}")
                print(f"   Name: {customer_name}")
                print(f"   Reason: {block_reason}")
                
                self.logger.info(f"Block detected for customer: {customer_name} ({customer_id})")
                
                return customer_id, customer_name, block_reason
            else:
                print("❌ Invalid format. Expected: CustomerID|CustomerName|BlockReason")
                return None, None, None
                
        except Exception as e:
            self.logger.error(f"Error parsing block detection input: {str(e)}")
            return None, None, None
import logging
import time
from datetime import datetime
from typing import Dict, Any

class ERPSimulator:
    """Simulates ERP system operations"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
    
    def create_sales_order(self, order_data: Dict[str, Any]) -> Dict[str, str]:
        """Simulate creating a sales order in ERP system"""
        try:
            self.logger.info("Creating sales order in ERP system...")
            
            # Simulate processing time
            time.sleep(2)
            
            # Generate order numbers
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            so_number = f"SO-{timestamp}"
            
            print(f"🔄 Creating Sales Order...")
            print(f"   Customer: {order_data.get('customer_name', 'Unknown')}")
            print(f"   Item: {order_data.get('item_description', 'Unknown')}")
            print(f"   SKU: {order_data.get('sku', 'Unknown')}")
            print(f"   Quantity: {order_data.get('quantity', '1')}")
            print(f"   Sales Order: {so_number}")
            
            self.logger.info(f"Sales order created: {so_number}")
            
            return {
                'sales_order_number': so_number,
                'status': 'created'
            }
            
        except Exception as e:
            self.logger.error(f"Error creating sales order: {str(e)}")
            raise
    
    def create_delivery_note(self, sales_order_number: str) -> Dict[str, str]:
        """Simulate creating delivery note"""
        try:
            self.logger.info("Creating delivery note...")
            
            # Simulate processing time
            time.sleep(1)
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            dn_number = f"DN-{timestamp}"
            
            print(f"📦 Creating Delivery Note: {dn_number}")
            
            self.logger.info(f"Delivery note created: {dn_number}")
            
            return {
                'delivery_note_number': dn_number,
                'status': 'created'
            }
            
        except Exception as e:
            self.logger.error(f"Error creating delivery note: {str(e)}")
            raise
    
    def create_invoice(self, delivery_note_number: str) -> Dict[str, str]:
        """Simulate creating invoice"""
        try:
            self.logger.info("Creating invoice...")
            
            # Simulate processing time
            time.sleep(1)
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            invoice_number = f"INV-{timestamp}"
            
            print(f"🧾 Creating Invoice: {invoice_number}")
            
            self.logger.info(f"Invoice created: {invoice_number}")
            
            return {
                'invoice_number': invoice_number,
                'status': 'created'
            }
            
        except Exception as e:
            self.logger.error(f"Error creating invoice: {str(e)}")
            raise
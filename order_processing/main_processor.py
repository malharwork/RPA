import os
import shutil
import logging
from datetime import datetime
from typing import List

from .text_extractor import TextExtractor
from .data_parser import DataParser
from .sku_mapper import SKUMapper
from .erp_simulator import ERPSimulator
from utils.email_sender import EmailSender

class OrderProcessor:
    """Main order processing workflow"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.text_extractor = TextExtractor(config_manager)
        self.data_parser = DataParser(config_manager)
        self.sku_mapper = SKUMapper(config_manager)
        self.erp_simulator = ERPSimulator(config_manager)
        self.email_sender = EmailSender(config_manager)
        
        # Folder paths
        self.input_folder = self.config.get('paths.input_folder', 'data/input')
        self.processed_folder = self.config.get('paths.processed_folder', 'data/processed')
        self.exceptions_folder = self.config.get('paths.exceptions_folder', 'data/exceptions')
    
    def run(self):
        """Execute the order processing workflow"""
        self.logger.info("Starting Order Processing workflow")
        print("\n🚀 Starting Order Processing Automation")
        print("=" * 50)
        
        try:
            # Get files to process
            files_to_process = self._get_files_to_process()
            
            if not files_to_process:
                print("📁 No files found in input folder")
                print(f"   Place PO files in: {self.input_folder}")
                return
            
            print(f"📄 Found {len(files_to_process)} files to process")
            
            # Process each file
            processed_count = 0
            exception_count = 0
            
            for file_path in files_to_process:
                try:
                    print(f"\n📋 Processing: {os.path.basename(file_path)}")
                    success = self._process_single_file(file_path)
                    
                    if success:
                        processed_count += 1
                    else:
                        exception_count += 1
                        
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {str(e)}")
                    self._move_to_exceptions(file_path, str(e))
                    exception_count += 1
            
            # Send completion summary
            self._send_completion_summary(processed_count, exception_count)
            
            print(f"\n✅ Order Processing Completed")
            print(f"   Processed: {processed_count}")
            print(f"   Exceptions: {exception_count}")
            
        except Exception as e:
            self.logger.error(f"Error in order processing workflow: {str(e)}")
            print(f"❌ Error: {str(e)}")
    
    def _get_files_to_process(self) -> List[str]:
        """Get list of files to process from input folder"""
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder, exist_ok=True)
            return []
        
        supported_formats = self.config.get('processing.supported_formats', ['.txt', '.pdf', '.jpg', '.jpeg', '.png'])
        files = []
        
        for filename in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in supported_formats:
                    files.append(file_path)
        
        return files
    
    def _process_single_file(self, file_path: str) -> bool:
        """Process a single file through the complete workflow"""
        try:
            # Step 1: Extract text
            print("   🔍 Extracting text...")
            extracted_text = self.text_extractor.extract_from_file(file_path)
            
            if not extracted_text.strip():
                raise ValueError("No text could be extracted from the file")
            
            # Step 2: Parse data
            print("   📊 Parsing order data...")
            parsed_order = self.data_parser.parse_text(extracted_text)
            
            # Step 3: Map SKU
            print("   🔗 Mapping SKU...")
            sku, sku_found = self.sku_mapper.map_item_to_sku(
                parsed_order.item_description, 
                parsed_order.customer_name
            )
            
            if not sku_found:
                raise ValueError(f"SKU mapping not found for item: {parsed_order.item_description}")
            
            # Step 4: Create ERP entries
            print("   💼 Creating ERP entries...")
            order_data = {
                'customer_name': parsed_order.customer_name,
                'item_description': parsed_order.item_description,
                'sku': sku,
                'quantity': parsed_order.quantity,
                'price': parsed_order.price
            }
            
            # Create sales order
            so_result = self.erp_simulator.create_sales_order(order_data)
            
            # Create delivery note
            dn_result = self.erp_simulator.create_delivery_note(so_result['sales_order_number'])
            
            # Create invoice
            inv_result = self.erp_simulator.create_invoice(dn_result['delivery_note_number'])
            
            # Step 5: Send notification to store
            self._send_store_notification(order_data, so_result, dn_result, inv_result)
            
            # Step 6: Move file to processed folder
            self._move_to_processed(file_path)
            
            print("   ✅ Processing completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            print(f"   ❌ Error: {str(e)}")
            self._move_to_exceptions(file_path, str(e))
            return False
    
    def _send_store_notification(self, order_data, so_result, dn_result, inv_result):
        """Send notification email to store team"""
        subject = f"New Order Ready for Delivery - {inv_result['invoice_number']}"
        
        body = f"""Order Details:
        
Customer: {order_data['customer_name']}
Item: {order_data['item_description']}
SKU: {order_data['sku']}
Quantity: {order_data['quantity']}

ERP References:
Sales Order: {so_result['sales_order_number']}
Delivery Note: {dn_result['delivery_note_number']}
Invoice: {inv_result['invoice_number']}

Please prepare for delivery.

Best regards,
RPA Automation System
"""
        
        store_emails = ["store@company.com"]  # Configure as needed
        self.email_sender.send_email(store_emails, subject, body)
    
    def _move_to_processed(self, file_path: str):
        """Move file to processed folder"""
        filename = os.path.basename(file_path)
        destination = os.path.join(self.processed_folder, filename)
        
        os.makedirs(self.processed_folder, exist_ok=True)
        shutil.move(file_path, destination)
        
        self.logger.info(f"File moved to processed: {destination}")
    
    def _move_to_exceptions(self, file_path: str, error_message: str):
        """Move file to exceptions folder with error log"""
        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exception_filename = f"{timestamp}_{filename}"
        destination = os.path.join(self.exceptions_folder, exception_filename)
        
        os.makedirs(self.exceptions_folder, exist_ok=True)
        shutil.move(file_path, destination)
        
        # Create error log file
        error_log_path = os.path.join(self.exceptions_folder, f"{timestamp}_{filename}.error.log")
        with open(error_log_path, 'w') as f:
            f.write(f"Error processing file: {filename}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Error: {error_message}\n")
        
        self.logger.warning(f"File moved to exceptions: {destination}")
    
    def _send_completion_summary(self, processed_count: int, exception_count: int):
        """Send completion summary email"""
        subject = f"Order Processing Summary - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = f"""Order Processing Automation Summary:

Processed Successfully: {processed_count} files
Exceptions/Errors: {exception_count} files
Total Files: {processed_count + exception_count}

Processing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Best regards,
RPA Automation System
"""
        
        admin_emails = ["admin@company.com"]  # Configure as needed
        self.email_sender.send_email(admin_emails, subject, body)
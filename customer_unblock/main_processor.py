import logging
from datetime import datetime

from .block_detector import BlockDetector
from .aging_report_generator import AgingReportGenerator
from .approval_manager import ApprovalManager
from .erp_unblock_manager import ERPUnblockManager
from .notification_manager import NotificationManager
from .request_tracker import RequestTracker

class CustomerUnblockProcessor:
    """Main customer unblock processing workflow"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.block_detector = BlockDetector(config_manager)
        self.aging_report_generator = AgingReportGenerator(config_manager)
        self.approval_manager = ApprovalManager(config_manager)
        self.erp_unblock_manager = ERPUnblockManager(config_manager)
        self.notification_manager = NotificationManager(config_manager)
        self.request_tracker = RequestTracker(config_manager)
    
    def run(self):
        """Execute the customer unblock workflow"""
        self.logger.info("Starting Customer Unblock workflow")
        print("\n🔓 Starting Customer Unblock Automation")
        print("=" * 50)
        
        try:
            # Step 1: Detect customer block
            customer_id, customer_name, block_reason = self.block_detector.detect_customer_block()
            
            if not customer_id:
                print("\n✅ No customer blocks detected. Process completed.")
                return
            
            # Generate unique request ID
            request_id = f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            print(f"\n🎫 Generated Request ID: {request_id}")
            
            # Log initial request
            self.request_tracker.log_request(request_id, customer_name, "PENDING_APPROVAL")
            
            # Step 2: Generate aging report
            print(f"\n📊 Generating aging report...")
            aging_report_path = self.aging_report_generator.generate_aging_report(
                customer_id, customer_name
            )
            
            # Step 3: Send approval request
            print(f"\n📧 Sending approval request to management...")
            approval_sent = self.approval_manager.send_approval_request(
                request_id, customer_name, block_reason, aging_report_path
            )
            
            if not approval_sent:
                print("❌ Failed to send approval request")
                self.request_tracker.log_request(request_id, customer_name, "FAILED_EMAIL")
                return
            
            # Update request status
            self.request_tracker.log_request(request_id, customer_name, "APPROVAL_SENT")
            
            # Step 4: Monitor for approval response
            print(f"\n⏳ Monitoring for approval response...")
            approval_status = self.approval_manager.monitor_approval_response(request_id)
            
            # Step 5: Process approval decision
            print(f"\n⚖️ Processing approval decision: {approval_status}")
            self._process_approval_decision(request_id, customer_id, customer_name, approval_status)
            
            print(f"\n✅ Customer Unblock Process Completed")
            print(f"   Request ID: {request_id}")
            print(f"   Final Status: {approval_status}")
            
        except Exception as e:
            self.logger.error(f"Error in customer unblock workflow: {str(e)}")
            print(f"❌ Error: {str(e)}")
    
    def _process_approval_decision(self, request_id: str, customer_id: str, 
                                 customer_name: str, approval_status: str):
        """Process the approval decision"""
        try:
            if approval_status == "APPROVED":
                print("✅ Request approved - processing unblock...")
                
                # Unblock customer in ERP
                unblock_success = self.erp_unblock_manager.unblock_customer(customer_id, customer_name)
                
                if unblock_success:
                    # Update status
                    self.request_tracker.log_request(request_id, customer_name, "APPROVED_COMPLETED")
                    
                    # Send approval notification
                    self.notification_manager.send_approval_notification(
                        customer_id, customer_name, request_id, "APPROVED"
                    )
                    
                    print("   ✅ Customer unblocked successfully")
                else:
                    self.request_tracker.log_request(request_id, customer_name, "UNBLOCK_FAILED")
                    print("   ❌ Failed to unblock customer in ERP")
            
            elif approval_status == "REJECTED":
                print("❌ Request rejected by management")
                
                # Update status
                self.request_tracker.log_request(request_id, customer_name, "REJECTED")
                
                # Send rejection notification
                self.notification_manager.send_approval_notification(
                    customer_id, customer_name, request_id, "REJECTED"
                )
                
                print("   📧 Rejection notification sent to sales team")
            
            else:  # TIMEOUT or unknown status
                print(f"⚠️ Unexpected status: {approval_status}")
                
                # Update status
                self.request_tracker.log_request(request_id, customer_name, f"TIMEOUT_{approval_status}")
                
                # Send timeout notification
                self.notification_manager.send_approval_notification(
                    customer_id, customer_name, request_id, approval_status
                )
                
                print("   📧 Timeout notification sent to admin team")
            
        except Exception as e:
            self.logger.error(f"Error processing approval decision: {str(e)}")
            self.request_tracker.log_request(request_id, customer_name, f"ERROR_{str(e)[:50]}")

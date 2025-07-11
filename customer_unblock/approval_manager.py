import logging
from datetime import datetime
from typing import List
from utils.email_sender import EmailSender

class ApprovalManager:
    """Manages the approval workflow for customer unblock requests"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.email_sender = EmailSender(config_manager)
    
    def send_approval_request(self, request_id: str, customer_name: str, 
                            block_reason: str, aging_report_path: str) -> bool:
        """Send approval request email to management"""
        try:
            self.logger.info(f"Sending approval request for: {customer_name}")
            
            # Get management emails from config
            management_emails = self.config.get('email.management_emails', ['manager@company.com'])
            
            subject = f"URGENT: Customer Unblock Request - {customer_name} (ID: {request_id})"
            
            body = f"""Dear Management Team,

We have received a new order for a blocked customer and require your approval to proceed.

Customer Details:
• Customer Name: {customer_name}
• Block Reason: {block_reason}
• Request ID: {request_id}
• Request Date: {datetime.now().strftime('%d-MMM-%Y %H:%M')}

Please review the attached aging report and respond with your decision:
• Reply 'APPROVED - {request_id}' to approve the unblock request
• Reply 'REJECTED - {request_id}' to reject the unblock request

The aging report is attached for your review.

Best regards,
RPA Automation System"""
            
            print(f"📧 Sending approval request to management...")
            success = self.email_sender.send_email(management_emails, subject, body, aging_report_path)
            
            if success:
                print(f"   ✅ Approval request sent successfully")
                self.logger.info(f"Approval request sent for request ID: {request_id}")
            else:
                print(f"   ⚠️ Email sending simulated (check configuration)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending approval request: {str(e)}")
            return False
    
    def monitor_approval_response(self, request_id: str) -> str:
        """Monitor for approval response - simulated with user input"""
        try:
            self.logger.info(f"Monitoring approval response for request: {request_id}")
            
            print(f"\n⏳ Waiting for Management Approval...")
            print("In a real system, this would monitor emails for approval responses.")
            print("For this POC, please simulate the management decision.")
            print()
            
            while True:
                response = input("Enter management decision (APPROVED/REJECTED): ").strip().upper()
                
                if response in ['APPROVED', 'REJECTED']:
                    print(f"✅ Decision received: {response}")
                    self.logger.info(f"Approval decision for {request_id}: {response}")
                    return response
                else:
                    print("❌ Invalid response. Please enter 'APPROVED' or 'REJECTED'")
                    
        except Exception as e:
            self.logger.error(f"Error monitoring approval response: {str(e)}")
            return "TIMEOUT"
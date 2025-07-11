import logging
from datetime import datetime
from utils.email_sender import EmailSender

class NotificationManager:
    """Manages notifications for customer unblock process"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.email_sender = EmailSender(config_manager)
    
    def send_approval_notification(self, customer_id: str, customer_name: str, 
                                 request_id: str, status: str) -> bool:
        """Send notification about approval decision"""
        try:
            if status == "APPROVED":
                subject = f"Customer Unblock APPROVED - {customer_name} (Request: {request_id})"
                
                body = f"""Dear Sales Team,

Good news! The customer unblock request has been APPROVED.

Customer Details:
• Customer Name: {customer_name}
• Customer ID: {customer_id}
• Request ID: {request_id}
• Approval Date: {datetime.now().strftime('%d-MMM-%Y %H:%M')}

The customer has been unblocked in the ERP system and you can now proceed with creating new sales orders.

Best regards,
RPA Automation System"""

            elif status == "REJECTED":
                subject = f"Customer Unblock REJECTED - {customer_name} (Request: {request_id})"
                
                body = f"""Dear Sales Team,

Unfortunately, the customer unblock request has been REJECTED by management.

Customer Details:
• Customer Name: {customer_name}
• Customer ID: {customer_id}
• Request ID: {request_id}
• Rejection Date: {datetime.now().strftime('%d-MMM-%Y %H:%M')}

Please contact the customer to discuss alternative payment arrangements before creating new orders.

Best regards,
RPA Automation System"""

            else:  # TIMEOUT or other status
                subject = f"Customer Unblock TIMEOUT - Manual Review Required - {customer_name}"
                
                body = f"""Dear Admin Team,

A customer unblock request requires manual review due to timeout or invalid response.

Customer Details:
• Customer Name: {customer_name}
• Customer ID: {customer_id}
• Request ID: {request_id}
• Status: {status}

Please review this request manually and take appropriate action.

Best regards,
RPA Automation System"""
            
            recipients = ["sales@company.com", "admin@company.com"]
            success = self.email_sender.send_email(recipients, subject, body)
            
            if success:
                self.logger.info(f"Notification sent for {status} decision: {request_id}")
                print(f"   📧 {status} notification sent to sales team")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
            return False
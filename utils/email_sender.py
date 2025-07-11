import smtplib
import ssl
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional

class EmailSender:
    """Handles email sending functionality"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Email configuration
        self.smtp_server = self.config.get('email.smtp_server', 'smtp.gmail.com')
        self.port = self.config.get('email.port', 587)
        self.sender_email = self.config.get('email.sender_email')
        self.sender_password = self.config.get('email.sender_password')
    
    def send_email(self, recipients: List[str], subject: str, body: str, 
                   attachment_path: Optional[str] = None) -> bool:
        """Send email with optional attachment"""
        
        if not self.sender_email or not self.sender_password:
            self.logger.warning("Email credentials not configured. Simulating email send.")
            self._simulate_email_send(recipients, subject, body, attachment_path)
            return True
        
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipients)
            message["Subject"] = subject
            
            # Add body to email
            message.attach(MIMEText(body, "plain"))
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                message.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                text = message.as_string()
                server.sendmail(self.sender_email, recipients, text)
            
            self.logger.info(f"Email sent successfully to: {', '.join(recipients)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            self._simulate_email_send(recipients, subject, body, attachment_path)
            return False
    
    def _simulate_email_send(self, recipients: List[str], subject: str, 
                           body: str, attachment_path: Optional[str] = None):
        """Simulate email sending for demo purposes"""
        print(f"\n📧 EMAIL SIMULATION")
        print(f"To: {', '.join(recipients)}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:100]}...")
        if attachment_path:
            print(f"Attachment: {attachment_path}")
        print("✅ Email simulation completed\n")
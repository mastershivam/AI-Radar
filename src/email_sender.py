import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from pathlib import Path
from dotenv import load_dotenv

class NewsletterSender:
    def __init__(self, smtp_server, smtp_port, email, password):
        """
        Initialize the newsletter sender.
        
        Args:
            smtp_server (str): SMTP server (e.g., 'smtp.gmail.com')
            smtp_port (int): SMTP port (e.g., 587 for TLS, 465 for SSL)
            email (str): Your email address
            password (str): Your email password or app password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_newsletter(self, to_emails, subject, html_content, text_content=None):
        """
        Send an HTML newsletter to multiple recipients.
        
        Args:
            to_emails (list): List of recipient email addresses
            subject (str): Email subject
            html_content (str): HTML content of the newsletter
            text_content (str): Plain text fallback (optional)
        """
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email
        msg['Subject'] = subject
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Add text content if provided
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
        
        # Send to each recipient
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(self.email, self.password)
            
            for recipient in to_emails:
                msg['To'] = recipient
                try:
                    server.send_message(msg)
                    print(f"✅ Newsletter sent to: {recipient}")
                except Exception as e:
                    print(f"❌ Failed to send to {recipient}: {e}")
    
    def send_newsletter_from_file(self, to_emails, subject, html_file_path, text_file_path=None):
        """
        Send a newsletter from HTML file.
        
        Args:
            to_emails (list): List of recipient email addresses
            subject (str): Email subject
            html_file_path (str): Path to HTML newsletter file
            text_file_path (str): Path to text version (optional)
        """
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            text_content = None
            if text_file_path and os.path.exists(text_file_path):
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            
            self.send_newsletter(to_emails, subject, html_content, text_content)
            
        except FileNotFoundError:
            print(f"❌ Newsletter file not found: {html_file_path}")
        except Exception as e:
            print(f"❌ Error sending newsletter: {e}")

def create_gmail_sender(email, app_password):
    """
    Create a Gmail sender using app password.
    
    Args:
        email (str): Your Gmail address
        app_password (str): Gmail app password (not your regular password)
    """
    return NewsletterSender('smtp.gmail.com', 587, email, app_password)

# Example usage

if __name__ == "__main__":
    
    load_dotenv()

    EMAIL = os.getenv('EMAIL_ADDRESS')
    APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')
    RECIPIENTS = [os.getenv('EMAIL_RECIPIENTS')]
    
   
    # Create sender
    sender = create_gmail_sender(EMAIL, APP_PASSWORD)
    
    # Send newsletter
    newsletter_file = "newsletter_2025-07-23.html"
    if os.path.exists(newsletter_file):
        sender.send_newsletter_from_file(
            to_emails=RECIPIENTS,
            subject="🤖 AI Radar Daily - July 23, 2025",
            html_file_path=newsletter_file
        )
    else:
        print(f"Newsletter file not found: {newsletter_file}") 
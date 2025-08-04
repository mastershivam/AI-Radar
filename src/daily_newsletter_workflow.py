#!/usr/bin/env python3
"""
Daily AI Newsletter Workflow
===========================

This script runs the complete daily newsletter workflow:
1. Pull new articles from all AI company blogs
2. Aggregate summaries for today
3. Generate HTML newsletter
4. Optionally send via email
"""

import os
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from utility_functions import run_data_pullers, aggregate_summaries, get_default_prompt
from newsletter_generator import create_newsletter_from_summary
from email_sender import create_gmail_sender

def run_daily_workflow(send_email=True):
    """
    Run the complete daily newsletter workflow.
    
    Args:
        send_email (bool): Whether to send the newsletter via email
    """
    
    print("🚀 Starting Daily AI Newsletter Workflow")
    print("=" * 50)
    
    # Step 1: Run all data pullers
    print("\n📡 Step 1: Pulling latest articles...")
    try:
        prompt = get_default_prompt()
        run_data_pullers(prompt)
        print("✅ All data pullers completed")
        
    except Exception as e:
        print(f"❌ Error running data pullers: {e}")
        return
    
    # Step 2: Aggregate summaries for today
    print("\n📊 Step 2: Aggregating today's summaries...")
    try:
        today = date.today()
        summary_file = aggregate_summaries(today.isoformat())
        print(f"✅ Summary aggregated: {summary_file}")
        
    except Exception as e:
        print(f"❌ Error aggregating summaries: {e}")
        return
    
    # Step 3: Generate HTML newsletter
    print("\n📧 Step 3: Generating HTML newsletter...")
    try:
        # Check if the summary file is empty
        if os.path.getsize(summary_file) == 0:
            print("❌ Error: The summary file is empty. No newsletter will be generated or sent.")
            return

        newsletter_file = create_newsletter_from_summary(summary_file, today.strftime("%B %d, %Y"))
        print(f"✅ Newsletter generated: {newsletter_file}")
        
    except Exception as e:
        print(f"❌ Error generating newsletter: {e}")
        return
    
    # Step 4: Send email (optional)
    if send_email:
        print("\n📤 Step 4: Sending newsletter via email...")
        try:
            # Load environment variables from .env file
            load_dotenv()
            
            # Get email credentials from .env file
            email = os.getenv('EMAIL_ADDRESS')
            app_password = os.getenv('EMAIL_APP_PASSWORD')
            recipients = [os.getenv('EMAIL_RECIPIENTS')]
            
            # Check if credentials are available
            if not email or not app_password or not recipients[0]:
                print("❌ Missing email credentials in .env file!")
                print("Make sure your .env file contains:")
                print("EMAIL_ADDRESS=your-email@gmail.com")
                print("EMAIL_APP_PASSWORD=your-16-character-app-password")
                print("EMAIL_RECIPIENTS=recipient@example.com")
                return
            
            # Create sender and send newsletter
            sender = create_gmail_sender(email, app_password)
            
            sender.send_newsletter_from_file(
                to_emails=recipients,
                subject=f"Your Daily Big Tech AI Digest - {today.strftime('%B %d, %Y')}",
                html_file_path=newsletter_file
            )
            print("✅ Newsletter sent successfully!")
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
    
    print("\n🎉 Daily newsletter workflow completed!")
    print(f"📁 Files created:")
    print(f"   - Summary: {summary_file}")
    print(f"   - Newsletter: {newsletter_file}")

def main():
    """Main function with example usage."""
    
    # Run the workflow with email sending enabled
    run_daily_workflow(send_email=True)

if __name__ == "__main__":
    main() 
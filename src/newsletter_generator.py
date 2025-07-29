import markdown
from datetime import datetime
from pathlib import Path

def generate_newsletter_html(summary_file_path, date_str=None):
    """
    Generate an HTML newsletter from a markdown summary file.
    
    Args:
        summary_file_path (str): Path to the markdown summary file
        date_str (str): Date string for the newsletter (defaults to today)
    
    Returns:
        str: HTML newsletter content
    """
    
    # Read the markdown content
    try:
        with open(summary_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        return f"<p>Summary file not found: {summary_file_path}</p>"
    
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)
    
    # Get date for newsletter
    if date_str is None:
        date_str = datetime.now().strftime("%B %d, %Y")
    
    # Create the HTML newsletter template
    html_newsletter = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily AI Digest - {date_str}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #000000;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .newsletter-container {{
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(90deg,rgba(75, 4, 110, 1) 0%, rgba(11, 44, 69, 1) 50%, rgba(20, 74, 40, 1) 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 42px;
            font-weight: 600;
        }}
        .header .date {{
            margin-top: 10px;
            opacity: 0.9;
            font-size: 16px;
        }}
        .content {{
            padding: 15px 20px;
        }}
        .content h1 {{
            color: #000000;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
        }}
        .content h2 {{
            color: #000000;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        .content p {{
            color: #000000; 
            margin-bottom: 10px;
        }}
        .article {{
            margin-bottom: 25px;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            border-radius: 4px;
        }}
        .article-title {{
            font-weight: bold;
            color: #000000;
            margin-bottom: 8px;
        }}
        .article-date {{
            color: #000000;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .article-url {{
            color: #3498db;  /* Change back to blue */
            text-decoration: none;
            font-size: 14px;
        }}
        .article-url:hover {{
            text-decoration: underline;
        }}
        .footer {{
            background-color: #ecf0f1;
            padding: 20px;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }}
        .footer a {{
            color: #3498db;
            text-decoration: none;
        }}
        .no-articles {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            padding: 40px 20px;
        }}
        @media only screen and (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .content {{
                padding: 20px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="newsletter-container">
        <div class="header">
            <h1> Daily AI Digest</h1>
            <div class="date">{date_str}</div>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer">
            <p>📧 This newsletter is automatically generated from Company Blog Feeds.</p>
            <p>🔗 <a href="https://github.com/mastershivam/ai-radar">View on GitHub</a>  
               
        </div>
    </div>
</body>
</html>
"""
    
    return html_newsletter

def save_newsletter_html(html_content, output_path):
    """Save the HTML newsletter to a file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Newsletter saved to: {output_path}")

def create_newsletter_from_summary(summary_file_path, date_str=None):
    """
    Create and save an HTML newsletter from a summary file.
    
    Args:
        summary_file_path (str): Path to the markdown summary file
        date_str (str): Date string for the newsletter
    """
    html_content = generate_newsletter_html(summary_file_path, date_str)
    
    # Generate output filename
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    output_path = f"Newsletters/newsletter_{date_str}.html"
    save_newsletter_html(html_content, output_path)
    
    return output_path

# Example usage
if __name__ == "__main__":
    # Create newsletter from today's summary
    summary_file = "daily_summary_2025-07-23.md"
    newsletter_file = create_newsletter_from_summary(summary_file, "July 23, 2025")
    print(f"Newsletter created: {newsletter_file}") 
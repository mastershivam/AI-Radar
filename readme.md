# AI Radar

A Python-based RSS feed aggregator and summarizer for AI company blogs and news sources. This project automatically fetches blog posts from various AI companies, summarizes them using local LLMs, generates beautiful HTML newsletters, and can send them via email.

## Features

- **Multi-source RSS Feed Processing**: Supports feeds from OpenAI, Anthropic, DeepMind, HuggingFace, and other AI companies
- **Local LLM Integration**: Uses Ollama with Mistral model for summarization
- **Duplicate Prevention**: Automatically skips articles already processed using URL-based detection
- **HTML Newsletter Generation**: Creates beautiful, responsive newsletters with modern styling
- **Email Automation**: Sends newsletters via SMTP with Gmail integration
- **Date-based Filtering**: Filter posts by specific dates or process all new articles
- **Markdown Output**: Generates clean, formatted summaries
- **Automated Processing**: Complete workflow from RSS feeds to email delivery

## Project Structure

```
AI Radar/
├── src/
│   ├── daily_newsletter_workflow.py  # Main orchestrator - complete workflow
│   ├── utility_functions.py          # Core utility functions
│   ├── newsletter_generator.py       # HTML newsletter generation
│   ├── email_sender.py              # Email sending functionality
│   ├── OpenAI_data_puller.py        # OpenAI blog post processor
│   ├── Anthropic_data_puller.py     # Anthropic blog post processor
│   ├── DeepMind_data_puller.py      # DeepMind blog post processor
│   ├── HuggingFace_data_puller.py   # HuggingFace data processor
│   ├── MetaAI_data_puller.py        # Meta AI blog post processor
│   └── PreventDuplicateSummaries.py # Duplicate detection utility
├── Markdown_Summaries/              # Individual RSS feed summaries
├── DailySummaries/                  # Aggregated daily summaries
├── Newsletters/                     # Generated HTML newsletters
├── .env                             # Email configuration (not in repo)
└── README.md                        # This file
```

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Mistral model downloaded in Ollama
- Gmail account with App Password (for email sending)

### Installing Ollama

1. **macOS/Linux:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Download Mistral model:**
   ```bash
   ollama pull mistral:latest
   ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AI-Radar
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install feedparser langchain-ollama python-dotenv markdown
   ```

4. **Set up email configuration:**
   Create a `.env` file in the root directory:
   ```bash
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_APP_PASSWORD=your-16-character-app-password
   EMAIL_RECIPIENTS=recipient@example.com
   ```

## Usage

### Complete Workflow (Recommended)

Run the complete daily newsletter workflow:
```bash
python src/daily_newsletter_workflow.py
```

This will:
1. Pull new articles from all AI company blogs
2. Aggregate summaries for today
3. Generate a beautiful HTML newsletter
4. Send the newsletter via email (if configured)

### Individual Components

**Run Data Pullers Only:**
```python
from utility_functions import run_data_pullers, get_default_prompt

prompt = get_default_prompt()
run_data_pullers(prompt)
```

**Aggregate Summaries:**
```python
from utility_functions import aggregate_summaries

# Aggregate for today
summary_file = aggregate_summaries()

# Aggregate for specific date
summary_file = aggregate_summaries('2025-07-29')
```

**Generate Newsletter:**
```python
from newsletter_generator import create_newsletter_from_summary

newsletter_file = create_newsletter_from_summary('daily_summary_2025-07-29.md')
```

**Send Email:**
```python
from email_sender import create_gmail_sender

sender = create_gmail_sender(email, app_password)
sender.send_newsletter_from_file(
    to_emails=['recipient@example.com'],
    subject='🤖 AI Radar Daily',
    html_file_path='newsletter_2025-07-29.html'
)
```

### Individual Feed Processing

**OpenAI Blog Posts:**
```python
from src.OpenAI_data_puller import OpenAI_BlogPost_Puller

prompt = "Access the link provided, summarise the blog post, and return a summary of the blog post in a couple of lines.\n"
OpenAI_BlogPost_Puller(prompt)
```

## Configuration

### Email Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Gmail → Settings → Security
   - Generate app password for "Mail"
3. **Create `.env` file:**
   ```bash
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_APP_PASSWORD=your-16-character-app-password
   EMAIL_RECIPIENTS=recipient@example.com
   ```

### Customization Options

- **LLM Model**: Change the Ollama model in the scripts (default: `mistral:latest`)
- **Summary Prompts**: Customize prompts in `utility_functions.py`
- **Newsletter Styling**: Modify CSS in `newsletter_generator.py`
- **Email Settings**: Configure SMTP settings in `email_sender.py`

## Output Format

### Markdown Summaries
Individual summaries are saved in `Markdown_Summaries/` with structure:
```markdown
---

Blog Post Title: [Title]
Date Published: [Date]
URL: [URL]

[Generated Summary]
```

### HTML Newsletters
Beautiful newsletters with:
- Responsive design
- Modern styling
- Company section headers
- Article summaries with links
- Professional footer

### Daily Aggregates
Combined summaries in `DailySummaries/` for specific dates.

## RSS Feed Sources

Currently supported feeds:
- **OpenAI**: `https://openai.com/news/rss.xml`
- **Anthropic**: `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml`
- **HuggingFace**: `https://huggingface.co/blog/feed.xml`
- **DeepMind**: `https://deepmind.com/blog/feed/basic`
- **Meta AI**: `https://rsshub.app/meta/ai/blog` (currently blocked by Cloudflare)

## Troubleshooting

### Common Issues

1. **Ollama not running:**
   ```bash
   ollama serve
   ```

2. **Model not found:**
   ```bash
   ollama pull mistral:latest
   ```

3. **Email authentication failed:**
   - Verify 2FA is enabled
   - Check app password is correct (16 characters)
   - Ensure `.env` file is properly formatted

4. **No summaries generated:**
   - Check if the specified date has any posts in the feed
   - Verify the RSS feed URL is accessible
   - Ensure the feed contains the expected date format

5. **Duplicate articles:**
   - The system automatically skips duplicates based on URL
   - Check `PreventDuplicateSummaries.py` for duplicate detection logic

### Debug Mode

Add debug prints to see available dates:
```python
for item in feed.entries:
    date = datetime(*item.published_parsed[:6], tzinfo=timezone.utc).date()
    print(f"Available date: {date}")
```

## Automation

### Cron Job Setup (macOS/Linux)

Add to crontab for daily execution:
```bash
0 8 * * * /path/to/venv/bin/python /path/to/AI\ Radar/src/daily_newsletter_workflow.py
```

### Windows Task Scheduler

Create a scheduled task to run:
```cmd
python src/daily_newsletter_workflow.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request




# AI Radar

A Python-based RSS feed aggregator and summarizer for AI company blogs and news sources. This project automatically fetches blog posts from various AI companies, summarizes them using local LLMs, and saves the results in markdown format.

## Features

- **Multi-source RSS Feed Processing**: Supports feeds from OpenAI, Anthropic, and other AI companies
- **Local LLM Integration**: Uses Ollama with Mistral model for summarization
- **Date-based Filtering**: Filter posts by specific dates
- **Markdown Output**: Generates clean, formatted summaries
- **Automated Processing**: Batch process multiple feeds and dates

## Project Structure

```
AI Radar/
├── src/
│   ├── main.py                    # Main entry point
│   ├── OpenAI_data_puller.py     # OpenAI blog post processor
│   ├── Anthropic_data_puller.py  # Anthropic blog post processor
│   └── HuggingFace_data_puller.py # HuggingFace data processor
├── Markdown_Summaries/           # Output directory for summaries
├── feed_anthropic.xml            # Local Anthropic RSS feed
├── daily_papers_*.md             # Daily paper summaries
└── README.md                     # This file
```

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Mistral model downloaded in Ollama

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
   pip install feedparser langchain-ollama
   ```

## Usage

### Basic Usage

Run the main script to process all feeds:
```bash
python src/main.py
```

### Individual Feed Processing

**OpenAI Blog Posts:**
```python
from src.OpenAI_data_puller import OpenAI_BlogPost_Puller
from datetime import date

# Process posts from a specific date
OpenAI_BlogPost_Puller(date=date(2025, 7, 25))
```

**Anthropic Blog Posts:**
```python
from src.Anthropic_data_puller import Anthropic_BlogPost_Puller
from datetime import date

# Process posts from a specific date
date_input = date(2025, 7, 21)
prompt = "Access the link provided, summarise the blog post, and return a summary of the blog post in a couple of lines.\n"
Anthropic_BlogPost_Puller(prompt, date_input)
```

### Configuration

You can customize the following parameters:

- **Date Filtering**: Specify exact dates to filter posts
- **LLM Model**: Change the Ollama model in the code (default: `mistral:latest`)
- **Output Directory**: Modify the output path in each script
- **Summary Prompts**: Customize the prompts used for summarization

## Output Format

Summaries are saved in markdown format with the following structure:

```markdown
---

Blog Post Title: [Title]
Date Published: [Date]
URL: [URL]

[Generated Summary]
```

## RSS Feed Sources

Currently supported feeds:
- **OpenAI**: `https://openai.com/news/rss.xml`
- **Anthropic**: `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml`
- **HuggingFace**: `https://huggingface.co/blog/feed.xml`

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

3. **No summaries generated:**
   - Check if the specified date has any posts in the feed
   - Verify the RSS feed URL is accessible
   - Ensure the feed contains the expected date format

### Debug Mode

Add debug prints to see available dates:
```python
for item in feed.entries:
    date = datetime(*item.published_parsed[:6], tzinfo=timezone.utc).date()
    print(f"Available date: {date}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request


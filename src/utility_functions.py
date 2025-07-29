#!/usr/bin/env python3
"""
Utility Functions for AI Radar
=============================

This module contains utility functions for data processing and aggregation.
"""

from datetime import date
from pathlib import Path
import os

def run_data_pullers(prompt):
    """
    Run all data pullers to fetch and summarize articles.
    
    Args:
        prompt (str): The prompt to use for summarization
    """
    from HuggingFace_data_puller import HuggingFace_BlogPost_Puller
    from OpenAI_data_puller import OpenAI_BlogPost_Puller
    from Anthropic_data_puller import Anthropic_BlogPost_Puller
    from DeepMind_data_puller import DeepMind_BlogPost_Puller
    # from MetaAI_data_puller import MetaAI_BlogPost_Puller  # Commented due to Cloudflare issues
    
    # Run all pullers
    HuggingFace_BlogPost_Puller(prompt)
    OpenAI_BlogPost_Puller(prompt)
    Anthropic_BlogPost_Puller(prompt)
    DeepMind_BlogPost_Puller(prompt)
    # MetaAI_BlogPost_Puller(prompt)  # Uncomment when RSSHub issues are resolved

def aggregate_summaries(target_date=None):
    """
    Aggregate summaries from all sources for a specific date.
    
    Args:
        target_date (str): Date to filter for (YYYY-MM-DD format)
    
    Returns:
        str: Path to the aggregated summary file
    """
    sources = [
        'Markdown_Summaries/openai_rss_summary.md',
        'Markdown_Summaries/deepmind_rss_summary.md',
        'Markdown_Summaries/anthropic_rss_summary.md',
        'Markdown_Summaries/hugging_faces_summary.md',
        'Markdown_Summaries/metaai_rss_summary.md'
    ]
    
    if target_date is None:
        target_date = date.today().isoformat()
    else:
        target_date = str(target_date)
    
    output_file = f'DailySummaries/daily_summary_{target_date}.md'
    
    with open(output_file, 'w') as out:
        for src in sources:
            try:
                with open(src, 'r') as f:
                    content = f.read()
                    # Split articles by separator
                    articles = content.split('\n\n---\n\n')
                    # Filter articles for the target date
                    todays_articles = [
                        a for a in articles if f'Date Published: {target_date}' in a
                    ]
                    if todays_articles:
                        # Extract the source name and format it nicely (e.g., "hugging_faces" -> "Hugging Faces", "openai" -> "OpenAI", "deepmind" -> "Google DeepMind")
                        src_name = src.split('/')[-1].replace('_rss_summary.md', '').replace('_summary.md', '').replace('_', ' ')
                        src_name = ' '.join([word.capitalize() for word in src_name.split()])
                        # Special cases
                        if src_name.lower() == "openai":
                            src_name = "OpenAI"
                        elif src_name.lower() == "deepmind":
                            src_name = "Google DeepMind"
                        out.write(f"# {src_name}\n")
                        out.write('\n\n---\n\n'.join(todays_articles))
                        out.write('\n\n')
            except FileNotFoundError:
                continue
    
    return output_file

def get_default_prompt():
    """
    Get the default prompt for article summarization.
    
    Returns:
        str: Default prompt
    """
    return "Access the link provided, summarise the blog post, and return a summary of the blog post in a couple of lines.\n"

def ensure_directory_exists(directory_path):
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path (str): Path to the directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)

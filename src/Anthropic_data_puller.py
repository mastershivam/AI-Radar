import feedparser
from datetime import datetime, timezone
from pathlib import Path
from langchain_ollama import ChatOllama
from PreventDuplicateSummaries import is_url_in_file

def Anthropic_BlogPost_Puller(prompt_input):
    rss_url = "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml"
    feed = feedparser.parse(rss_url)

    output_path = Path("Markdown_Summaries/Anthropic_rss_summary.md")
    new_summaries = 0

    for item in feed.entries:
        url = item.get("link") or item.get("guid")
        title = item.title
        published_date = datetime(*item.published_parsed[:6], tzinfo=timezone.utc).date()

        if is_url_in_file(url, output_path):
            print(f"Skipped duplicate: {url}")
            continue

        prompt = prompt_input + f"Title: {title}\nURL: {url}\n"
        llm = ChatOllama(model="mistral:latest")
        summary = llm.invoke(prompt).content

        with open(output_path, "a") as f:
            f.write("\n\n---\n\n")
            f.write(f"**Blog Post Title: {title}**<br>\n")
            f.write(f"Date Published: {published_date}<br>\n")
            f.write(f"URL: {url}<br>\n\n")
            f.write(summary)
        new_summaries += 1
        print(f"Added summary for: {url}")

    print(f"Saved {new_summaries} new summaries to {output_path}")



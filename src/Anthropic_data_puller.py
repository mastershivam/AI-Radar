import feedparser
from datetime import datetime, timezone, date
from pathlib import Path
from langchain_ollama import ChatOllama

def Anthropic_BlogPost_Puller(prompt_input,date_to_filter=date.today()):
    rss_url = "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml"
    feed = feedparser.parse(rss_url)

    summaries = []

    for item in feed.entries:
        prompt=prompt_input
        url = item.get("link") or item.get("guid")
        published_date = datetime(*item.published_parsed[:6], tzinfo=timezone.utc).date()

        if published_date == date_to_filter:
            title = item.title
            prompt += (
                f"Title: {title}\n"
                f"URL: {url}\n"
            )
            
            llm = ChatOllama(model="mistral:latest")
            summary = llm.invoke(prompt).content

            summaries.append({
                "title": title,
                "url": url,
                "pubdate": published_date,
                "summary": summary
            })

    # Save as markdown
    output_path = Path("Markdown_Summaries/Anthropic_rss_summary.md")
    with open(output_path, "a") as f:
        for entry in summaries:
            f.write("\n\n---\n\n")
            f.write(f"Blog Post Title: {entry['title']}\n")
            f.write(f"Date Published: {entry['pubdate']}\n")
            f.write(f"URL: {entry['url']}\n\n")
            f.write(entry['summary'])

    print(f"Saved {len(summaries)} summaries to {output_path}")



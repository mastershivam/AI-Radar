import feedparser
from datetime import datetime, timezone,date
from langchain_ollama import ChatOllama

def HuggingFace_BlogPost_Puller(prompt_input,date_to_filter=date.today()):
    rss_url = "https://huggingface.co/blog/feed.xml"
    feed = feedparser.parse(rss_url)

    for i,item in enumerate(feed.entries,1):
        # Prefer link but fallback to guid
        url = item.get("link") or item.get("guid")
        
        prompt=prompt_input
        # Parse published date
        date = datetime(*item.published_parsed[:6], tzinfo=timezone.utc).date()
        

        if date == date_to_filter:
            prompt += f"   Title: {item.title}\n"
            prompt += f"   URL: {url}\n"
        
            llm = ChatOllama(model="mistral:latest")
            summary = llm.invoke(prompt)
            summary.content   


            with open(f"Markdown_Summaries/hugging_faces_summary.md","a") as f:
                f.write('\n\n---\n\n')
                f.write(f'Blog Post Title: {item.title}\n')
                f.write(f'Date Published: {date}\n')
                f.write(f'URL: {url}\n')
                f.write(summary.content)
                print('Article written to HuggingFace file')

        
 

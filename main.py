# main.py
import praw
import json
from datetime import datetime
from google.cloud import storage

from google.cloud import secretmanager

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/ai-radar-465910/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
    
def fetch_reddit_posts(request):
    reddit = praw.Reddit(
        client_id=get_secret("reddit-client-id"),
        client_secret=get_secret("reddit-client-secret"),
        username=get_secret("reddit-username"),
        password=get_secret("reddit-password"),
        user_agent="AI Radar by u/your_username"
    )

    posts = []
    for submission in reddit.subreddit("MachineLearning+LLM").hot(limit=10):
        posts.append({
            "title": submission.title,
            "url": submission.url,
            "score": submission.score,
            "created": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
            "subreddit": submission.subreddit.display_name
        })

    # Save to GCS
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("data_storage_ai_radar")
    blob = bucket.blob(f"reddit/posts_{datetime.now().isoformat()}.json")
    blob.upload_from_string(json.dumps(posts), content_type="application/json")

    return f"Uploaded {len(posts)} posts."
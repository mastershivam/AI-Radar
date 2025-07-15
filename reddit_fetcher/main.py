import praw
import json
import logging
import time
from datetime import datetime
from flask import Flask, request, jsonify
from google.cloud import storage
from google.cloud import secretmanager

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_secret(secret_id):
    logging.info(f"Fetching secret: {secret_id}")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/ai-radar-465910/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

@app.route("/", methods=["POST", "GET"])
def fetch_reddit_posts():
    try:
        start_time = time.time()

        logging.info("🔐 Retrieving secrets...")
        client_id = get_secret("reddit-client-id")
        client_secret = get_secret("reddit-client-secret")
        username = get_secret("reddit-username")
        password = get_secret("reddit-password")

        logging.info("Authenticating with Reddit...")
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent="AI Radar by u/your_username"
        )

        logging.info("Fetching posts from Reddit...")
        posts = []
        for submission in reddit.subreddit("MachineLearning+LLM").hot(limit=10):
            posts.append({
                "title": submission.title,
                "url": submission.url,
                "score": submission.score,
                "created": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                "subreddit": submission.subreddit.display_name
            })

        logging.info(f"Fetched {len(posts)} posts.")

        logging.info("💾 Uploading to GCS...")
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("data_storage_ai_radar")
        filename = f"reddit/posts_{datetime.now().isoformat()}.json"
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(posts), content_type="application/json")

        elapsed = round(time.time() - start_time, 2)
        logging.info(f"🎉 Done in {elapsed}s → {filename}")
        return jsonify({"message": f"Uploaded {len(posts)} posts in {elapsed}s."})

    except Exception as e:
        logging.error(f"🔥 ERROR: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
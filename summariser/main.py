# main.py
import os
import json
from datetime import datetime
from google.cloud import storage, aiplatform_v1,aiplatform_v1beta1,aiplatform
from flask import Flask, request, jsonify
from vertexai.language_models import TextGenerationModel

app = Flask(__name__)

# Initialize Vertex AI
PROJECT_ID = os.environ.get("PROJECT_ID")
REGION = os.environ.get("REGION", "europe-west1")
aiplatform.init(project=PROJECT_ID, location=REGION)

# Model settings
MODEL_NAME = "text-bison@002"  # Change to gemini-pro when needed


def load_reddit_posts_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string()
    return json.loads(content)


def build_prompt(posts):
    prompt = (
        "You are an AI researcher. Summarize today's Reddit discussions from AI-related subreddits.\n"
        "Summarize the content in 3–5 bullet points, highlighting trends, tools, breakthroughs, or controversies.\n\n"
    )
    for i, post in enumerate(posts):
        prompt += f"POST {i+1}:\nTitle: {post['title']}\nURL: {post['url']}\nContent: {post.get('selftext', 'No body')}\n\n"
    prompt += "\nGive a professional summary."
    return prompt


def call_vertex_ai(prompt):
    model = TextGenerationModel.from_pretrained(MODEL_NAME)
    response = model.predict(prompt=prompt, temperature=0.4, max_output_tokens=512)
    return response.text


def save_summary_to_gcs(summary_text, bucket_name, date_str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"summaries/summary_{date_str}.json")
    blob.upload_from_string(json.dumps({"summary": summary_text}), content_type="application/json")


@app.route("/", methods=["POST"])
def summarize_handler():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing or invalid JSON in request."}), 400

        bucket_name = data.get("bucket")
        file_name = data.get("file")
        if not bucket_name or not file_name:
            return jsonify({"error": "Missing bucket or file name in request."}), 400

        date_str = datetime.now().strftime("%Y-%m-%d")
        posts = load_reddit_posts_from_gcs(bucket_name, file_name)
        prompt = build_prompt(posts)
        summary = call_vertex_ai(prompt)
        save_summary_to_gcs(summary, bucket_name, date_str)

        return jsonify({"message": f"Summary saved for {date_str}", "summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
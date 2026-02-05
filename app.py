from flask import Flask, request, jsonify
from google import genai
import json
import os

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    message = data.get("message")

    prompt = f"""
Check if this message is a scam.

Message:
{message}

Return ONLY JSON:
{{"classification":"SCAM or SAFE","confidence":1-100,"reason":"short explanation"}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.candidates[0].content.parts[0].text.strip()

        return jsonify(json.loads(text))

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":

    app.run()
    @app.route("/")
    def home():
        return "AI Honeypot API is running"


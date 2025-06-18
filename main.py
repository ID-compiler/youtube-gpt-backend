from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    transcript = data.get("transcript", "")

    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following transcript from a YouTube video:\n\n{transcript}"
                }
            ],
            max_tokens=700,
            temperature=0.5
        )
        notes = response.choices[0].message.content
        return jsonify({"notes": notes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS
import logging
logging.basicConfig(level=logging.INFO)

# Configure API key from Railway environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("WARNING: GOOGLE_API_KEY not set. Using mock responses only.")
else:
    genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

@app.route("/improve", methods=["POST"])

def improve():
    logging.info("Received a request")
    data = request.json
    logging.info(f"Data: {data}")
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # If API_KEY is missing, return mock response
    if not API_KEY:
        return jsonify({"improved_prompt": f"{prompt} [mock improved]"}), 200

    # Real Gemini API call with error handling
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are an AI prompt optimizer. Rewrite the following prompt to make it clearer, more specific, and structured to get the best AI answer: {prompt}"
        )
        improved = response.candidates[0].content.parts[0].text
        return jsonify({"improved_prompt": improved})
    except Exception as e:
        # Catch any Gemini API errors and keep app alive
        return jsonify({"error": f"Gemini API failed: {str(e)}"}), 500

# Optional: handle favicon requests to prevent repeated 502s
@app.route("/favicon.ico")
def favicon():
    return "", 204

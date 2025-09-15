from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

# Configure API key from Railway environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/improve", methods=["POST"])
def improve():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"You are an AI prompt optimizer. Rewrite the following prompt to make it clearer and more specific: {prompt}"
        )
        improved = response.candidates[0].content.parts[0].text
        return jsonify({"improved_prompt": improved})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/favicon.ico")
def favicon():
    return "", 204

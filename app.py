from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/improve", methods=["POST"])
def improve():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        f"You are an AI prompt optimizer. Take the following user prompt and rewrite it so it is clearer, more specific, and structured in a way that will elicit the best possible answer from an AI model. - Keep the meaning and intent of the original prompt. - Add helpful context, details, or structure if they are missing. - Only output the improved prompt itself.: {prompt}"
    )

    improved = response.candidates[0].content.parts[0].text
    return jsonify({"improved_prompt": improved})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

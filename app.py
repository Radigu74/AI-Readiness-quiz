from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Use the new OpenAI client (v1.0+)
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json

        prompt = f"""
You are an expert AI readiness evaluator.

Based on these answers, classify the business into one of:
- "AI-Ready"
- "In Progress"
- "Early Stage"

Instructions:
- Look for automation use, data usage, and team confidence as indicators.
- AI-Ready means strong on most or all areas.
- In Progress means some areas are strong, others need work.
- Early Stage means minimal use or confidence in AI or data.

Return ONLY valid JSON like this:
{{
  "readiness": "In Progress",
  "message": "You're making progress on AI, with some good early efforts. Let's build momentum.",
  "ctaText": "Book a free strategy session",
  "ctaLink": "https://calendly.com/your-link"
}}

Answers:
1. {data['q1']}
2. {data['q2']}
3. {data['q3']}
4. {data['q4']}
5. {data['q5']}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_result = response.choices[0].message.content.strip()

        # Safely parse GPT JSON-like reply
        try:
            result = json.loads(raw_result)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON from GPT"}), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask app running at http://127.0.0.1:5000")
    app.run(debug=True)

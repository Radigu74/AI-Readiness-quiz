from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
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
        Based on the answers below, determine the AI readiness level (choose: "AI-Ready", "In Progress", or "Early Stage").
        Then write a short summary message and a matching CTA.

        Answers:
        1. {data['q1']}
        2. {data['q2']}
        3. {data['q3']}
        4. {data['q4']}
        5. {data['q5']}

        Return JSON like:
        {{
          "readiness": "AI-Ready",
          "message": "You're ahead of the curve!",
          "ctaText": "Book a free strategy session",
          "ctaLink": "https://calendly.com/your-link"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Safely parse GPT JSON-like reply
        raw_result = response.choices[0].message.content.strip()
        result = eval(raw_result)  # ⚠️ You may replace with json.loads if strict JSON returned

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask app running at http://127.0.0.1:5000")
    app.run(debug=True)

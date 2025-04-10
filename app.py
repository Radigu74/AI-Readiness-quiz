from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
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
      "readiness": "In Progress",
      "message": "...",
      "ctaText": "...",
      "ctaLink": "https://calendly.com/your-link"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content

        return jsonify(eval(result))  # ⚠️ assuming safe JSON-like format

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Flask is running at http://127.0.0.1:5000")
    app.run(debug=True)

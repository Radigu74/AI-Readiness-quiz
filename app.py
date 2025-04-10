from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    prompt = f"""
    Based on the answers below, determine the AI readiness level (AI-Ready, In Progress, Early Stage),
    give a short message and a CTA, and include a 3-bullet summary in markdown.

    Answers:
    1. {data['q1']}
    2. {data['q2']}
    3. {data['q3']}
    4. {data['q4']}
    5. {data['q5']}

    Return as JSON like:
    {{
      "readiness": "...",
      "message": "...",
      "ctaText": "...",
      "ctaLink": "https://yourcalendar.com",
      "summary": "..."
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    result = eval(response.choices[0].message.content)
    return jsonify(result)

if __name__ == "__main__":
    print("🚀 Starting Flask server...")    
    app.run(debug=True)


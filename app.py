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

        # Full context to help GPT understand all possible answers

        system_message = """
You are an expert AI Readiness Evaluator.

Your job is to analyze answers to a 5-question quiz and classify the business into one of 3 AI readiness stages:

- "AI-Ready": strong use of automation & data, confident team, prior AI use.
- "In Progress": some progress in automation, digital processes, or exploration.
- "Early Stage": limited digital processes, no AI use, unsure team.

Each question uses consistent options. Here is what they mean:

1. Automation use:
    - "extensive" → advanced automation in multiple areas
    - "some" → partial or isolated automation
    - "none" → manual processes mostly

2. Team confidence with AI:
    - "high" → the team is excited and skilled
    - "medium" → some team members open to AI, some unsure
    - "low" → team lacks interest, trust, or knowledge

3. Use of data:
    - "active" → the company uses data for decisions or automation
    - "collect" → data is gathered but not used
    - "none" → no structured data collected

4. AI tool experience:
    - "yes" → already using tools like ChatGPT, Notion AI, etc.
    - "testing" → trying AI tools experimentally
    - "no" → no experience with AI tools

5. Main challenge:
    - "use_case" → unsure how AI fits the business
    - "skills" → lack of skills, time, or team resources
    - "trust" → concerns about ethics, data privacy, accuracy
    - "starting" → just beginning digital transformation

---

🎯 Based on the answers, return ONLY this exact JSON structure below, and wrap it in triple backticks like a code block:

```json
{
    "readiness": "AI-Ready",
    "message": "Amazing work — your business is clearly ahead in adopting AI! Let’s keep the conversation going.",
    "ctaText": "Contact Us",
    "ctaLink": "https://www.terrapeakgroup.com/contact-form"
}
```

⚠️ Do **not** include any text outside of the above code block.
"""
        user_prompt = f"""
        Answers:
        1. {data['q1']}
        2. {data['q2']}
        3. {data['q3']}
        4. {data['q4']}
        5. {data['q5']}
        """
    
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]
        )

        raw_result = response.choices[0].message.content.strip()
        print("🔥 GPT raw output:\n", raw_result)

        # Extract JSON from triple backticks using regex
        import re
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_result, re.DOTALL)
        if match:
            raw_json = match.group(1)
            result = json.loads(raw_json)
        else:
            print("❌ Failed to extract JSON from GPT output.")
            return jsonify({"error": "GPT did not return valid JSON"}), 500

        return jsonify(result)

    except Exception as e:
        print("❗ Backend error:", e)
        return jsonify({"error": str(e)}), 500






   




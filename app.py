from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
import markdown

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# AI Mentor System Prompt
SYSTEM_PROMPT = """
You are AI Mentor.

IMPORTANT RULES:

- Explain concepts in simple words.
- Use proper markdown formatting.
- Use headings.
- Use bullet points.
- Use short paragraphs.
- Give 2 real-world examples.
- Highlight important terms.
- Never return huge walls of text.

Always follow this structure:

# Topic Name

## Definition
Explanation

## Key Points
- Point 1
- Point 2
- Point 3

## Real-World Examples

### Example 1
Explanation

### Example 2
Explanation

## Summary
Short summary
"""

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "")

        prompt = f"""
{SYSTEM_PROMPT}

User Question:
{user_message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # Convert markdown to HTML
        formatted_response = markdown.markdown(
            response.text,
            extensions=["extra"]
        )

        return jsonify({
            "response": formatted_response
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "response":
            "<p>⚠️ AI Mentor is currently unavailable. Please try again later.</p>"
        })


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
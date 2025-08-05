import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

def evaluate_description(word: str, translation: str, example: str, user_input: str) -> dict:
    prompt = f"""
The goal is to evaluate how well a user understands the given word.

**Word:** {word}
**Translation:** {translation}
**Example Sentence:** {example}

**User Input:** {user_input}

Rate how well the input describes the word. Return only the following JSON:

{{
  "score": 1–5,  // 1 = poor, 5 = excellent
  "feedback": "short feedback text for the user"
}}

Respond only in JSON format, no explanations.
"""

    response = model.generate_content(prompt)
    try:
        text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(text)
    except Exception as e:
        return {"score": 1, "feedback": f"Fehler bei Bewertung: {str(e)}"}
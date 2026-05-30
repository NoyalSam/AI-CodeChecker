import os
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

load_dotenv()

app = Flask(__name__)

# ── LLM setup (from user's notebook) ──────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
)

# ── Chain 1: Error Detector ────────────────────────────────────────────────────
detector_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert static code analyzer.
Analyze the given code and detect ALL errors.

Return ONLY a valid JSON object with this exact structure:
{{
  "has_errors": true or false,
  "language": "detected language",
  "error_count": number,
  "errors": [
    {{
      "line": line_number_or_null,
      "severity": "Critical | High | Medium | Low",
      "type": "Syntax Error | Runtime Error | Security Issue | Logical Error | Performance Issue | Code Quality",
      "description": "clear explanation",
      "wrong_code": "the problematic snippet"
    }}
  ],
  "summary": "one sentence overall assessment"
}}

If no errors exist, set has_errors to false and errors to [].
Return ONLY the JSON. No markdown, no extra text.""",
    ),
    ("human", "Analyze this code:\n\n{code}"),
])

detector_chain = detector_prompt | llm | StrOutputParser()

# ── Chain 2: Code Fixer ────────────────────────────────────────────────────────
fixer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert software engineer.
You receive a code snippet and a JSON analysis of its errors.
Your job: return the fully corrected, optimized, production-ready code.

Rules:
- Fix EVERY error listed in the analysis
- Preserve original logic and intent
- Add brief inline comments only where genuinely helpful
- Do NOT wrap in markdown fences
- Return ONLY the corrected source code, nothing else""",
    ),
    (
        "human",
        "Original code:\n\n{code}\n\nError analysis:\n{analysis}\n\nReturn the corrected code only:",
    ),
])

fixer_chain = fixer_prompt | llm | StrOutputParser()


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.json.get("code", "").strip()
    if not code:
        return {"error": "No code provided"}, 400

    try:
        # Step 1: detect errors
        analysis_raw = detector_chain.invoke({"code": code})

        # Clean up any accidental markdown fences
        clean = analysis_raw.strip()
        if clean.startswith("```"):
            clean = "\n".join(clean.split("\n")[1:])
        if clean.endswith("```"):
            clean = "\n".join(clean.split("\n")[:-1])

        analysis = json.loads(clean)

        # Step 2: if errors found, get corrected code
        corrected_code = None
        if analysis.get("has_errors"):
            corrected_code = fixer_chain.invoke({
                "code": code,
                "analysis": json.dumps(analysis, indent=2),
            })

        return {
            "analysis": analysis,
            "corrected_code": corrected_code,
        }

    except json.JSONDecodeError as e:
        return {"error": f"LLM returned invalid JSON: {str(e)}", "raw": analysis_raw}, 500
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

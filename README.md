# 🔍 CodeScan — AI-Powered Code Reviewer

An intelligent code review web application powered by **Google Gemini 2.5 Flash** and **LangChain**. Paste any code, click Scan, and get instant error detection with a fully corrected version — all in a clean dark-themed UI.

---

## 📸 Features

- ✅ Detects **Syntax Errors, Runtime Errors, Security Issues, Logical Errors, Performance Issues, and Code Quality** problems
- ✅ Shows **severity level** for each error — Critical, High, Medium, Low
- ✅ Shows **exact line numbers** where errors occur
- ✅ Returns **fully corrected, production-ready code**
- ✅ Supports **all programming languages** — Python, JavaScript, Java, C++, and more
- ✅ **Two-stage LangChain prompt chain** — one LLM detects, another LLM fixes
- ✅ Clean **split-panel dark UI** with copy button

---

## 🏗️ Project Structure

```
code_reviewer/
├── app.py                  # Flask backend — chains, routes, logic
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── templates/
    └── index.html          # Frontend UI
```

---

## ⚙️ How It Works

The app uses a **two-stage LangChain pipe chain**:

```
User pastes code
      ↓
Chain 1 — Error Detector
  RunnablePassthrough → detector_prompt → Gemini LLM → StrOutputParser
  Returns: JSON with errors, severity, line numbers, types
      ↓
Chain 2 — Code Fixer (only runs if errors found)
  RunnablePassthrough → fixer_prompt → Gemini LLM → StrOutputParser
  Returns: fully corrected source code
      ↓
Both results sent back to browser and displayed
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/code-reviewer.git
cd code-reviewer
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
```

Open `.env` and add your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

> Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. Run the app

```bash
python app.py
```

Open your browser and go to:

```
http://localhost:5000
```

---

## 🖥️ Usage

1. Paste your code into the **left panel**
2. Click the **Scan** button (or press `Ctrl + Enter`)
3. View detected errors in the **top right panel** — with severity badges and line numbers
4. View the **corrected code** in the **bottom right panel**
5. Click **Copy** to copy the fixed code

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Flask | Web server and routing |
| LangChain | LLM chain orchestration |
| LangChain Google GenAI | Gemini model connector |
| Google Gemini 2.5 Flash | AI model for detection and fixing |
| python-dotenv | Secure API key management |
| HTML / CSS / JavaScript | Frontend UI |

---

## 📦 Dependencies

```
flask>=3.0.0
python-dotenv>=1.0.0
langchain-google-genai>=1.0.0
langchain-core>=0.2.0
```

---

## 🔐 Security Note

- Never commit your `.env` file to GitHub
- The `.env.example` file is safe to commit — it contains no real keys
- Add `.env` to your `.gitignore` file

### Recommended `.gitignore`

```
.env
__pycache__/
*.pyc
venv/
.venv/
```

---

## 📁 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the main UI |
| POST | `/analyze` | Accepts `{"code": "..."}`, returns analysis + corrected code |

### Example request

```json
POST /analyze
Content-Type: application/json

{
  "code": "a = 10\nb = 20\nprin(a + b)"
}
```

### Example response

```json
{
  "analysis": {
    "has_errors": true,
    "language": "Python",
    "error_count": 1,
    "errors": [
      {
        "line": 3,
        "severity": "High",
        "type": "Runtime Error",
        "description": "prin is not defined. The correct function is print.",
        "wrong_code": "prin(a + b)"
      }
    ],
    "summary": "1 runtime error found — misspelled built-in function."
  },
  "corrected_code": "a = 10\nb = 20\nprint(a + b)"
}
```

---

## 🙌 Acknowledgements

- [LangChain](https://www.langchain.com/) — LLM orchestration framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) — AI model
- [Flask](https://flask.palletsprojects.com/) — Python web framework

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

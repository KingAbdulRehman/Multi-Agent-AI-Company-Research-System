# 🔬 AI Company Research Agent

A portfolio-grade **Multi-Agent AI system** that researches any company and
produces a professional PDF intelligence report — powered by **CrewAI**,
**Gemini 1.5 Flash**, and a slick **Chainlit** chat UI.

```
User types company name
        ↓
Agent 1 (Researcher)  →  searches the web via Serper API
        ↓
Agent 2 (Analyst)     →  identifies strengths, risks, opportunities
        ↓
Agent 3 (Writer)      →  writes executive-level business report
        ↓
Beautiful PDF report  +  Chainlit chat display
```

---

## Project Structure

```
ai-company-research/
├── app.py                  # Chainlit UI entry point
├── crew/
│   ├── __init__.py
│   ├── agents.py           # Agent 1, 2, 3 definitions
│   ├── tasks.py            # Task prompts for each agent
│   └── crew.py             # Sequential crew orchestration
├── tools/
│   ├── __init__.py
│   └── search_tool.py      # Serper web-search tool
├── utils/
│   ├── __init__.py
│   └── pdf_generator.py    # ReportLab PDF generation
├── output/                 # PDF reports saved here
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 1. Virtual Environment Setup

### Windows (PowerShell or CMD)
```bash
# Create venv
python -m venv venv

# Activate
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

---

## 2. How to Get Your Free API Keys

### Gemini API Key (Google AI Studio — FREE)
1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select **"Create API key in new project"** (or use existing)
5. Copy the key — it starts with `AIza…`
6. **Free tier:** 15 requests/min, 1M tokens/day — more than enough

### Serper API Key (FREE Google Search for AI)
1. Go to **https://serper.dev**
2. Click **"Get Started Free"**
3. Sign up with email (no credit card required)
4. After signup you land on the **Dashboard**
5. Copy your API key from the top of the dashboard
6. **Free tier:** 2,500 searches/month — plenty for demos

---

## 3. Installation and Running

### Step 1 — Clone / download the project
```bash
# If using git
git clone <your-repo-url>
cd ai-company-research

# Or just cd into the project folder
cd "Multi-Agent AI Company Research System"
```

### Step 2 — Create your `.env` file
```bash
# Copy the example
cp .env.example .env

# Edit .env and paste your keys
# Windows: notepad .env
# Mac/Linux: nano .env
```

Your `.env` should look like:
```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SERPER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```
> Installation takes 2-3 minutes — CrewAI pulls several ML libraries.

### Step 4 — Run the app
```bash
chainlit run app.py
```

The app opens at **http://localhost:8000** automatically.

---

## 4. Testing with 3 Companies

Once the app is running, try these in order — they make great demo material:

### Test 1: Tesla
```
Tesla
```
Expected: ~2-3 min research time, covers EVs, FSD, Elon Musk, competitors (BYD, Rivian), recent recalls/news.

### Test 2: OpenAI
```
OpenAI
```
Expected: GPT-4/o1 products, $157B valuation, Sam Altman, Microsoft partnership, Anthropic/Google competition.

### Test 3: Stripe
```
Stripe
```
Expected: Payment infrastructure, $50B valuation, Patrick/John Collison, Adyen/Braintree competition, recent product launches.

**Each test generates a PDF in the `/output` folder.**

---

## 5. What to Show in Your Loom Video (Maximum Client Impression)

### Recommended recording flow (8-10 minutes):

**[0:00–0:30] — The Problem**
> "Researching a company manually takes 2-3 hours. This system does it in 3 minutes using 3 AI agents working as a team."

**[0:30–1:30] — Project Walkthrough**
- Show the folder structure briefly
- Open `crew/agents.py` — highlight the 3 agents and their roles
- Open `crew/tasks.py` — show the detailed task prompts
- Open `app.py` — point out the real-time progress callbacks

**[1:30–2:00] — Start the App**
```bash
chainlit run app.py
```
Show the browser opening at localhost:8000.

**[2:00–5:00] — LIVE DEMO (most important part)**
- Type `Tesla` and hit Enter
- Narrate each progress update as it appears:
  - *"Now Agent 1 is using Serper to search Google in real time…"*
  - *"Agent 2 is reading that research and identifying business insights…"*
  - *"Agent 3 is writing the executive report from the analysis…"*
- Show the console/terminal (split screen) where you can see agents "thinking" in verbose mode

**[5:00–6:30] — Show the Report**
- Scroll through the full report in the chat UI
- Point out: Executive Summary, Health Score, Strengths, Risks
- Click the PDF download button — open the PDF and show the professional layout

**[6:30–7:30] — Run a Second Company**
- Type `OpenAI` — let it run while you talk about the architecture
- Show it completes and generates a different, accurate report

**[7:30–8:30] — Architecture Explanation**
> "This uses CrewAI's sequential process — each agent gets the previous agent's output as context. Gemini 1.5 Flash is free, Serper gives us real Google results, and ReportLab generates the PDF. The whole system is containerized with Docker."

**[8:30–9:00] — Close**
> "Full source code on GitHub, ready to deploy to any cloud platform."

### Power tips for the video:
- Use a dark terminal theme (looks more professional)
- Keep the browser and terminal side-by-side
- Zoom into the health score in the PDF — clients love a clear number
- If an agent "thinks out loud" in the console, read a few lines — shows the AI reasoning

---

## 6. Common Errors and Fixes

### ❌ `GEMINI_API_KEY not set` or `AuthenticationError`
**Fix:** Make sure your `.env` file is in the project root (same folder as `app.py`), not inside a subfolder. Double-check the key value has no spaces.

### ❌ `SerperAPIException` or `SERPER_API_KEY not found`
**Fix:** Same as above — check `.env`. Also verify you haven't exceeded the 2,500 free monthly searches on serper.dev dashboard.

### ❌ `ModuleNotFoundError: No module named 'crewai'`
**Fix:** Your virtual environment isn't activated. Run:
```bash
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
# Then install again
pip install -r requirements.txt
```

### ❌ `LiteLLMException: BadRequestError` or `RateLimitError`
**Fix:** Gemini free tier allows 15 RPM. If you're testing rapidly, wait 60 seconds. For production, add `time.sleep(5)` between tests or upgrade to a paid key.

### ❌ `chainlit: command not found`
**Fix:** Chainlit wasn't installed in your active venv. Run `pip install chainlit` in the activated venv.

### ❌ `RecursionError` or agent loops forever
**Fix:** The `max_iter=3` on each agent prevents infinite loops. If you still see it, check that your task `expected_output` is concrete — vague expected outputs confuse agents.

### ❌ PDF opens but looks empty / garbled
**Fix:** The report text came back in an unexpected format. Open the terminal and check the raw `result` variable. Usually caused by a Gemini rate-limit mid-task returning a partial response.

### ❌ Chainlit shows no download button for PDF
**Fix:** Check that the `/output` folder exists and the app has write permissions. On Windows, run the terminal as Administrator if needed.

### ❌ `TypeError: 'str' object is not callable` in callbacks
**Fix:** This is a Python 3.9 issue with `list[str]` type hints in `pdf_generator.py`. Use Python 3.10 or 3.11:
```bash
python --version  # must be 3.10+
```

---

## Docker Deployment

```bash
# Build image
docker build -t ai-research-agent .

# Run with your API keys
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e SERPER_API_KEY=your_key \
  -v $(pwd)/output:/app/output \
  ai-research-agent
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Multi-agent framework | CrewAI | Orchestrates 3 specialist agents |
| LLM | Gemini 1.5 Flash | Powers all 3 agents (free tier) |
| Web search | Serper API | Real Google results for Agent 1 |
| Chat UI | Chainlit | Real-time streaming progress UI |
| PDF generation | ReportLab | Professional downloadable reports |
| Environment | python-dotenv | Secure API key management |

---

*Built as a portfolio project demonstrating multi-agent AI orchestration.*
*Perfect for companies needing automated competitive intelligence.*

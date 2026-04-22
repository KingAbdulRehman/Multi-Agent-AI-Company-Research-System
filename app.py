"""Chainlit entry point for the AI Company Research Agent."""

import asyncio
import os
import time

from dotenv import load_dotenv

# ── Load env vars BEFORE any crewai / langchain imports ───────────────────────
load_dotenv()

# LiteLLM (used internally by CrewAI) expects GEMINI_API_KEY.
# Support users who set GOOGLE_API_KEY instead.
if not os.getenv("GEMINI_API_KEY") and os.getenv("GOOGLE_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

# ── Now it's safe to import the crew modules ──────────────────────────────────
import chainlit as cl

from crew.crew import ResearchCrew
from utils.pdf_generator import generate_pdf


WELCOME = """# 🔬 AI Company Research Agent

Welcome! I'm your AI-powered business intelligence assistant backed by **3 specialist AI agents**.

| Agent | Role | Job |
|-------|------|-----|
| 🔍 Agent 1 | Senior Research Analyst | Searches the web for company data |
| 📊 Agent 2 | Business Strategy Analyst | Identifies strengths, risks & opportunities |
| ✍️ Agent 3 | Report Writer | Produces an executive-level business report |

**Output:** Full report in chat + downloadable PDF with Business Health Score

---

**Just type a company name and press Enter!**

Examples: `Tesla` · `OpenAI` · `Stripe` · `Nvidia` · `Anthropic` · `SpaceX`
"""


# ── Chainlit lifecycle ────────────────────────────────────────────────────────

@cl.on_chat_start
async def start():
    await cl.Message(content=WELCOME).send()


@cl.on_message
async def main(message: cl.Message):
    company = message.content.strip()

    if len(company) < 2:
        await cl.Message(
            content="⚠️ Please enter a valid company name (at least 2 characters)."
        ).send()
        return

    start_time = time.time()
    loop       = asyncio.get_running_loop()

    # ── Kick-off banner ───────────────────────────────────────────────────────
    await cl.Message(
        content=f"🚀 Starting research on **{company}**. This usually takes **2–4 minutes**…"
    ).send()

    # ── Mutable progress messages ─────────────────────────────────────────────
    step1 = cl.Message(content=f"🔍 **Agent 1 (Researcher)** — searching for **{company}** data…")
    await step1.send()

    step2 = cl.Message(content="⏳ **Agent 2 (Analyst)** — waiting for research to finish…")
    await step2.send()

    step3 = cl.Message(content="⏳ **Agent 3 (Writer)** — waiting for analysis to finish…")
    await step3.send()

    # ── Thread-safe UI update helper ──────────────────────────────────────────
    def schedule(coro):
        asyncio.run_coroutine_threadsafe(coro, loop)

    async def _upd(msg: cl.Message, text: str):
        msg.content = text
        await msg.update()

    # ── Callbacks fired from the crew worker thread ───────────────────────────
    def on_research_done():
        schedule(_upd(step1, f"✅ **Agent 1** — research on **{company}** complete"))
        schedule(_upd(step2, "📊 **Agent 2 (Analyst)** — analysing the data…"))

    def on_analysis_done():
        schedule(_upd(step2, "✅ **Agent 2** — strategic analysis complete"))
        schedule(_upd(step3, "✍️ **Agent 3 (Writer)** — writing the professional report…"))

    def on_writing_done():
        schedule(_upd(step3, "✅ **Agent 3** — report written"))

    # ── Run crew in thread pool (keeps async event loop unblocked) ────────────
    crew = ResearchCrew(
        company_name=company,
        on_research_done=on_research_done,
        on_analysis_done=on_analysis_done,
        on_writing_done=on_writing_done,
    )

    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(None, crew.run),
            timeout=600,  # 10-minute hard limit
        )
    except asyncio.TimeoutError:
        await cl.Message(
            content=(
                "⏰ **Timeout** — the research took too long (> 10 min).\n\n"
                "Try a more well-known company or check your API quotas."
            )
        ).send()
        return
    except Exception as exc:
        await cl.Message(
            content=(
                f"❌ **Error during research:** `{exc}`\n\n"
                "Please verify your `GEMINI_API_KEY` and `SERPER_API_KEY` in `.env`, then try again."
            )
        ).send()
        return

    # ── Generate PDF ──────────────────────────────────────────────────────────
    pdf_msg = cl.Message(content="📄 **Generating PDF report…**")
    await pdf_msg.send()

    pdf_path = None
    try:
        pdf_path = await loop.run_in_executor(None, generate_pdf, company, result)
        pdf_msg.content = "✅ **PDF report generated!**"
        await pdf_msg.update()
    except Exception as exc:
        pdf_msg.content = f"⚠️ **PDF generation failed:** `{exc}`"
        await pdf_msg.update()

    # ── Display full report ───────────────────────────────────────────────────
    await cl.Message(content=f"## 📋 Research Report: {company}\n\n{result}").send()

    # ── PDF download button ───────────────────────────────────────────────────
    if pdf_path and os.path.exists(pdf_path):
        safe_name = company.replace(" ", "_")
        elements  = [
            cl.File(
                name=f"{safe_name}_report.pdf",
                path=pdf_path,
                display="inline",
            )
        ]
        await cl.Message(
            content=f"📥 **Download your PDF report for {company}:**",
            elements=elements,
        ).send()

    # ── Timing summary ────────────────────────────────────────────────────────
    elapsed        = time.time() - start_time
    mins, secs     = divmod(int(elapsed), 60)
    time_str       = f"{mins}m {secs}s" if mins else f"{secs}s"
    await cl.Message(content=f"⏱️ **Total research time:** {time_str}").send()

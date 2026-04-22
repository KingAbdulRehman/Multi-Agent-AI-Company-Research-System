"""Task definitions for the three-agent research pipeline."""

from crewai import Task
from crewai import Agent


def create_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Conduct thorough web research on the company: **{company}**.\n\n"
            "You MUST search for and compile all of the following:\n"
            "1. **Company Overview** — founding year, headquarters, legal name, mission/vision, industry/sector\n"
            "2. **Products & Services** — flagship offerings, key features, pricing tiers (if available)\n"
            "3. **Leadership Team** — CEO and at least 3 other C-suite executives with brief bios\n"
            "4. **Financials** — latest funding round or revenue figures, total funding raised, "
            "   valuation, employee headcount\n"
            "5. **Recent News** — at least 5 significant developments from the last 6 months "
            "   (launches, partnerships, acquisitions, controversies, etc.)\n"
            "6. **Market Position** — top 3 direct competitors, estimated market share, "
            "   differentiators vs competitors\n\n"
            "Use multiple targeted searches. Prioritise official sources, reputable press, "
            "and financial databases. Compile everything into a structured document."
        ),
        expected_output=(
            "A well-structured research document about {company} with clearly labelled sections:\n"
            "- Company Overview\n"
            "- Products and Services\n"
            "- Leadership Team\n"
            "- Financial Overview\n"
            "- Recent News (last 6 months)\n"
            "- Market Position and Competitors\n\n"
            "All facts must be specific and grounded in search results."
        ),
        agent=agent,
    )


def create_analysis_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Using the research document about **{company}** provided by the researcher, "
            "perform a rigorous strategic analysis.\n\n"
            "Your analysis MUST include:\n"
            "1. **Top 3 Strengths** — specific competitive advantages backed by evidence\n"
            "2. **Top 3 Risks / Weaknesses** — concrete vulnerabilities the company faces\n"
            "3. **Market Position Analysis** — how {company} stands relative to competitors, "
            "   moat strength, pricing power\n"
            "4. **Business Opportunities** — 2-3 growth opportunities the company should pursue, "
            "   with rationale\n"
            "5. **Business Health Score** — a score from 1 to 10 with a detailed justification "
            "   referencing specific data points. Format EXACTLY as: "
            "   'Business Health Score: X/10'\n\n"
            "Be analytical, specific, and data-driven. Avoid generic statements."
        ),
        expected_output=(
            "A strategic analysis document for {company} containing:\n"
            "- Top 3 Strengths (with evidence)\n"
            "- Top 3 Risks / Weaknesses (with evidence)\n"
            "- Market Position Analysis\n"
            "- Business Opportunities (2-3 items)\n"
            "- Business Health Score: X/10 (with full justification)\n\n"
            "All insights must be specific, evidence-based, and tied to the research data."
        ),
        agent=agent,
    )


def create_writing_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Using the research and strategic analysis about **{company}**, write a complete, "
            "professional business intelligence report.\n\n"
            "The report MUST contain ALL of the following sections, each with a markdown "
            "## heading:\n\n"
            "## Executive Summary\n"
            "(3-4 punchy sentences covering who {company} is, what it does, and the key takeaway)\n\n"
            "## Company Overview\n"
            "(Founding story, HQ, mission, industry, size)\n\n"
            "## Products and Services\n"
            "(Core offerings, key features, target customers, pricing if known)\n\n"
            "## Leadership Team\n"
            "(CEO and key executives with short bios)\n\n"
            "## Financial Overview\n"
            "(Funding, revenue, valuation, employee count)\n\n"
            "## Recent News and Developments\n"
            "(5+ notable events from the last 6 months)\n\n"
            "## Market Position and Competition\n"
            "(Competitive landscape, market share, differentiators)\n\n"
            "## Strengths and Opportunities\n"
            "(Top strengths + growth opportunities)\n\n"
            "## Risks and Weaknesses\n"
            "(Key vulnerabilities and threats)\n\n"
            "## Overall Assessment and Recommendation\n"
            "(Actionable recommendation: invest / partner / monitor / avoid — with reasoning)\n\n"
            "## Conclusion\n"
            "(Summary paragraph + Business Health Score prominently stated as 'Business Health Score: X/10')\n\n"
            "Write in a professional, executive tone. Use bullet points inside sections where "
            "appropriate. Ensure the Business Health Score appears clearly in the Conclusion."
        ),
        expected_output=(
            "A complete, professionally written business intelligence report about {company} "
            "with all 11 sections (## headings), specific data points throughout, strategic "
            "insights, clear recommendation, and a prominently stated Business Health Score: X/10 "
            "in the Conclusion. Minimum 800 words."
        ),
        agent=agent,
    )

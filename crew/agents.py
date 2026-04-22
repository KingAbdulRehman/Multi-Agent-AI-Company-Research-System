"""Three specialist agents for the company research pipeline."""

import os
from crewai import Agent, LLM
from tools.search_tool import get_search_tool


def _get_llm() -> LLM:
    """Return a configured Gemini 2.0 Flash LLM via LiteLLM."""
    return LLM(
        model="gemini/gemini-2.5-flash-lite",
        temperature=0.7,
        max_tokens=4096,
    )


def create_researcher() -> Agent:
    return Agent(
        role="Senior Research Analyst",
        goal=(
            "Find comprehensive, accurate, and up-to-date information about {company} "
            "including its history, products, leadership, financials, and recent news."
        ),
        backstory=(
            "You are an elite corporate researcher with 15+ years of experience tracking "
            "companies across every sector. You know exactly which queries surface the most "
            "useful data, and you verify facts before including them. You use web search "
            "methodically — starting with overviews, then drilling into specifics like "
            "funding rounds, executive changes, and product launches from the last 6 months."
        ),
        tools=[get_search_tool()],
        llm=_get_llm(),
        verbose=True,
        max_iter=3,
        allow_delegation=False,
    )


def create_analyst() -> Agent:
    return Agent(
        role="Business Strategy Analyst",
        goal=(
            "Analyse the research gathered about {company} and produce sharp strategic "
            "insights: top strengths, key risks, competitive positioning, growth "
            "opportunities, and an evidence-based business health score out of 10."
        ),
        backstory=(
            "You are a seasoned strategy consultant who has advised Fortune 500 companies "
            "and high-growth startups alike. You cut through noise to identify what truly "
            "drives a company's performance, where it is vulnerable, and which market "
            "opportunities it should pursue. Your business health scores are respected "
            "industry-wide for their rigour and objectivity."
        ),
        tools=[],
        llm=_get_llm(),
        verbose=True,
        max_iter=3,
        allow_delegation=False,
    )


def create_writer() -> Agent:
    return Agent(
        role="Professional Business Report Writer",
        goal=(
            "Transform the research and analysis about {company} into a polished, "
            "executive-ready business report that is clear, structured, and actionable."
        ),
        backstory=(
            "You have written hundreds of board-level intelligence reports for private "
            "equity firms, investment banks, and corporate strategy teams. Your reports "
            "are famous for combining density of information with crystal-clear prose. "
            "You always open with a punchy executive summary and close with a concrete "
            "recommendation tied to the business health score."
        ),
        tools=[],
        llm=_get_llm(),
        verbose=True,
        max_iter=3,
        allow_delegation=False,
    )

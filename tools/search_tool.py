from crewai_tools import SerperDevTool


def get_search_tool() -> SerperDevTool:
    """Return a configured SerperDev search tool.

    Creating it lazily (inside a function) ensures the SERPER_API_KEY is already
    loaded from .env before the tool tries to validate the key.
    """
    return SerperDevTool()

"""Crew orchestration — sequential pipeline of 3 agents."""

from crewai import Crew, Process

from crew.agents import create_analyst, create_researcher, create_writer
from crew.tasks import create_analysis_task, create_research_task, create_writing_task


class ResearchCrew:
    """Runs the three-agent research pipeline for a given company.

    Optional callbacks are called (from the worker thread) after each task
    completes, allowing the Chainlit UI to update progress in real time.
    """

    def __init__(
        self,
        company_name: str,
        on_research_done=None,
        on_analysis_done=None,
        on_writing_done=None,
    ):
        self.company_name      = company_name
        self.on_research_done  = on_research_done
        self.on_analysis_done  = on_analysis_done
        self.on_writing_done   = on_writing_done
        self._completed        = 0

    def _task_callback(self, task_output) -> None:
        """Called by CrewAI after each task finishes (sequential order)."""
        idx = self._completed
        self._completed += 1

        handlers = [self.on_research_done, self.on_analysis_done, self.on_writing_done]
        if idx < len(handlers) and handlers[idx]:
            try:
                handlers[idx]()
            except Exception:
                pass  # never crash the worker thread over a UI callback

    def run(self) -> str:
        """Build and kick off the crew; return the final report as a string."""
        researcher = create_researcher()
        analyst    = create_analyst()
        writer     = create_writer()

        research_task  = create_research_task(researcher)
        analysis_task  = create_analysis_task(analyst)
        writing_task   = create_writing_task(writer)

        crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=True,
            task_callback=self._task_callback,
        )

        result = crew.kickoff(inputs={"company": self.company_name})
        return str(result)

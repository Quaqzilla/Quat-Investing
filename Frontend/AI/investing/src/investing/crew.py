from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from investing.tools.search import search
import os
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from crewai_tools import (
    FirecrawlSearchTool
)

@CrewBase
class Investing():
    """Investing crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def news_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['economic_news_simplifier'], # type: ignore[index]
            verbose=True,
            cache = True,
            tools = [FirecrawlSearchTool('fc-6772e20d9c0c414d9e02ec433ea8f896')]
        )

    @task
    def analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['economic_news_research_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Investing crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

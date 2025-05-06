from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
import os
import google.generativeai as genai

@CrewBase
class WebscraperCrew:
    """Webscraper Crew"""

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    llm = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.7
        )

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper'],
			tools=[ScrapeWebsiteTool()],
            llm=self.llm,
            allow_delegation=False,
			verbose=True
        )
    
    @task
    def scrape_website(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_website'],
            agent=self.scraper()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Webscraper crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
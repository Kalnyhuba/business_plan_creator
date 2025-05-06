from typing import Optional
from crewai import Agent, Crew, Task, Process
from pydantic import BaseModel

class BusinessPlanVerification(BaseModel):
    valid: bool
    feedback: Optional[str]

class ReviewBusinessPlanCrew():
    """ReviewBusinessPlan crew"""

    def __init__(self, agents_config, tasks_config, llm):
        self.agents_config = agents_config
        self.tasks_config = tasks_config
        self.llm = llm
        self.agents = self.create_agents()
        self.tasks = self.create_tasks()
        self.crew = self.create_crew()

    def create_agents(self):
        business_plan_reviewer = Agent(
            role=self.agents_config["business_plan_reviewer"]["role"],
            goal=self.agents_config["business_plan_reviewer"]["goal"],
            backstory=self.agents_config["business_plan_reviewer"]["backstory"],
            verbose=True,
            llm=self.llm
        )
        return [business_plan_reviewer]

    def create_tasks(self):
        review_business_plan = Task(
            description=self.tasks_config["review_business_plan"]["description"],
            expected_output=self.tasks_config["review_business_plan"]["expected_output"],
            agent=self.agents[0],
            output_pydantic=BusinessPlanVerification
        )
        return [review_business_plan]

    def create_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def review_plan(self, business_plan_content: str):
        """Review a business plan and return the verification result"""
        # Create a new task with the business plan content
        review_task = Task(
            description=f"{self.tasks_config['review_business_plan']['description']}\n\nBusiness Plan to Review:\n{business_plan_content}",
            expected_output=self.tasks_config["review_business_plan"]["expected_output"],
            agent=self.agents[0],
            output_pydantic=BusinessPlanVerification
        )
        
        # Create a new crew with just this task
        review_crew = Crew(
            agents=self.agents,
            tasks=[review_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Run the review
        result = review_crew.kickoff()
        return result

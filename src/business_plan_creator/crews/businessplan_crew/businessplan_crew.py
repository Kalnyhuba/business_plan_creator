from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
import google.generativeai as genai

@CrewBase
class BusinessPlanCrew:
    """Business Plan Crew"""

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    llm = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.7
        )

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def business_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['business_designer'],
            llm=self.llm,
			verbose=True
        )
    
    @agent
    def product_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['product_designer'],
            llm=self.llm,
			verbose=True
        )
    
    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst'],
            llm=self.llm,
			verbose=True
        )
    
    @agent
    def marketing_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['marketing_expert'],
            llm=self.llm,
			verbose=True
        )
    
    @agent
    def operations_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['operations_specialist'],
            llm=self.llm,
			verbose=True
        )
    
    @agent
    def financial_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_expert'],
            llm=self.llm,
			verbose=True
        )
    
    @task
    def create_business_concept(self) -> Task:
        return Task(
            config=self.tasks_config['create_business_concept'],
            agent=self.business_designer()
        )
    
    @task
    def create_product_design(self) -> Task:
        return Task(
            config=self.tasks_config['create_product_design'],
            context=["create_business_concept"],
            agent=self.product_designer()
        )
    
    @task
    def create_market_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['create_market_analysis'],
            context=["create_business_concept", "create_product_design"],
            agent=self.market_analyst()
        )
    
    @task
    def create_marketing_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_marketing_plan'],
            context=["create_business_concept", "create_market_analysis", "create_product_design"],
            agent=self.marketing_expert()
        )
    
    @task
    def create_operating_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_operating_plan'],
            context=["create_business_concept", "create_market_analysis", "create_product_design", "create_marketing_plan"],
            agent=self.operations_specialist()
        )
    
    @task
    def create_financial_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_financial_plan'],
            context=["create_business_concept", "create_market_analysis", "create_product_design", "create_marketing_plan", "create_operating_plan"],
            agent=self.financial_expert()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BusinessPlan crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

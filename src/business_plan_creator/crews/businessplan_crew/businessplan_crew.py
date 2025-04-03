from crewai import Agent, Crew, Task, Process

class BusinessPlanCrew:
    """Business Plan Crew"""

    def __init__(self, agents_config, tasks_config, llm):
        self.agents_config = agents_config
        self.tasks_config = tasks_config
        self.llm = llm
        self.agents = self.create_agents()
        self.tasks = self.create_tasks()
        self.crew = self.create_crew()

    def create_agents(self):
        business_designer = Agent(
            role=self.agents_config["business_designer"]["role"],
            goal=self.agents_config["business_designer"]["goal"],
            backstory=self.agents_config["business_designer"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        market_analyst = Agent(
            role=self.agents_config["market_analyst"]["role"],
            goal=self.agents_config["market_analyst"]["goal"],
            backstory=self.agents_config["market_analyst"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        competition_analyst = Agent(
            role=self.agents_config["competition_analyst"]["role"],
            goal=self.agents_config["competition_analyst"]["goal"],
            backstory=self.agents_config["competition_analyst"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        product_designer = Agent(
            role=self.agents_config["product_designer"]["role"],
            goal=self.agents_config["product_designer"]["goal"],
            backstory=self.agents_config["product_designer"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        marketing_expert = Agent(
            role=self.agents_config["marketing_expert"]["role"],
            goal=self.agents_config["marketing_expert"]["goal"],
            backstory=self.agents_config["marketing_expert"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        operations_specialist = Agent(
            role=self.agents_config["operations_specialist"]["role"],
            goal=self.agents_config["operations_specialist"]["goal"],
            backstory=self.agents_config["operations_specialist"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        financial_expert = Agent(
            role=self.agents_config["financial_expert"]["role"],
            goal=self.agents_config["financial_expert"]["goal"],
            backstory=self.agents_config["financial_expert"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        stakeholder = Agent(
            role=self.agents_config["stakeholder"]["role"],
            goal=self.agents_config["stakeholder"]["goal"],
            backstory=self.agents_config["stakeholder"]["backstory"],
            verbose=True,
            llm=self.llm
        )

        return [business_designer, market_analyst, competition_analyst, product_designer, marketing_expert, operations_specialist, financial_expert, stakeholder]

    def create_tasks(self):
        create_business_concept = Task(
            description=self.tasks_config["create_business_concept"]["description"],
            expected_output=self.tasks_config["create_business_concept"]["expected_output"],
            agent=self.agents[0]
        )

        create_market_analysis = Task(
            description=self.tasks_config["create_market_analysis"]["description"],
            expected_output=self.tasks_config["create_market_analysis"]["expected_output"],
            agent=self.agents[1],
            context=[create_business_concept]
        )

        create_competition_analysis = Task(
            description=self.tasks_config["create_competition_analysis"]["description"],
            expected_output=self.tasks_config["create_competition_analysis"]["expected_output"],
            agent=self.agents[2],
            context=[create_business_concept, create_market_analysis]
        )

        create_product_design = Task(
            description=self.tasks_config["create_product_design"]["description"],
            expected_output=self.tasks_config["create_product_design"]["expected_output"],
            agent=self.agents[3],
            context=[create_business_concept, create_market_analysis, create_competition_analysis]
        )

        create_marketing_plan = Task(
            description=self.tasks_config["create_marketing_plan"]["description"],
            expected_output=self.tasks_config["create_marketing_plan"]["expected_output"],
            agent=self.agents[4],
            context=[create_business_concept, create_market_analysis, create_competition_analysis, create_product_design] 
        )

        create_operating_plan = Task(
            description=self.tasks_config["create_operating_plan"]["description"],
            expected_output=self.tasks_config["create_operating_plan"]["expected_output"],
            agent=self.agents[5],
            context=[create_business_concept, create_market_analysis, create_competition_analysis, create_product_design, create_marketing_plan]
        )

        create_financial_plan = Task(
            description=self.tasks_config["create_financial_plan"]["description"],
            expected_output=self.tasks_config["create_financial_plan"]["expected_output"],
            agent=self.agents[6],
            context=[create_business_concept, create_market_analysis, create_competition_analysis, create_product_design, create_marketing_plan, create_operating_plan]
        )

        create_investor_assessment = Task(
            description=self.tasks_config["create_investor_assessment"]["description"],
            expected_output=self.tasks_config["create_investor_assessment"]["expected_output"],
            agent=self.agents[7],
            context=[create_business_concept, create_market_analysis, create_competition_analysis, create_product_design, create_marketing_plan, create_operating_plan, create_financial_plan]
        )

        return [create_business_concept, create_market_analysis, create_competition_analysis, create_product_design, create_marketing_plan, create_operating_plan, create_financial_plan, create_investor_assessment]

    def create_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

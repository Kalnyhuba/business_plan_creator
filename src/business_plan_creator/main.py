#!/usr/bin/env python
import yaml
from typing import Dict
from pydantic import BaseModel
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from business_plan_creator.crews.businessplan_crew.businessplan_crew import BusinessPlanCrew

class BusinessPlanState(BaseModel):
    business_concept: str = ""
    business_plan_content: str = ""

class BusinessPlanFlow(Flow[BusinessPlanState]):

    @start()
    def get_user_input(self):
        """Get input from the user about the business concept"""
        print("\n=== Create Your Business Plan ===\n")
        self.state.business_concept = input("What business concept would you like to create a business plan for? ")
        print(f"\nCreating a business plan for {self.state.business_concept}...\n")
        return self.state
    
    @listen(get_user_input)
    def create_business_plan(self, state: BusinessPlanState):
        """Create the business plan using the crew with DeepSeek LLM"""
        print("Creating business plan...")

        # Initialize the LLM
        llm = LLM(
            model="ollama/deepseek-r1",
            base_url="http://localhost:11434"
        )

        # Load configurations
        with open("src/business_plan_creator/crews/businessplan_crew/config/agents.yaml", "r") as f:
            agents_config = yaml.safe_load(f)
        
        with open("src/business_plan_creator/crews/businessplan_crew/config/tasks.yaml", "r") as f:
            tasks_config = yaml.safe_load(f)

        # Create and run the crew
        crew = BusinessPlanCrew(agents_config, tasks_config, llm)
        result = crew.crew.kickoff(inputs={"business_idea": state.business_concept})
        
        state.business_plan_content = result.raw

        print("\nBusiness plan creation completed successfully")
        return "Business plan creation completed successfully"


def kickoff():
    """Run the business plan creator flow"""
    BusinessPlanFlow().kickoff()
    print("\n=== Flow Complete ===")


def plot():
    """Generate a visualization of the flow"""
    flow = BusinessPlanFlow()
    flow.plot("business_plan_creator_flow")
    print("Flow visualization saved to business_plan_creator_flow.html")


if __name__ == "__main__":
    kickoff()

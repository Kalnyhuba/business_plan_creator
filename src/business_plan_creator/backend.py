from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import LLM
import yaml
from .crews.businessplan_crew.businessplan_crew import BusinessPlanCrew
from typing import List, Dict
import os
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class BusinessPlanRequest(BaseModel):
    business_concept: str

class AgentResponse(BaseModel):
    role: str
    content: str

class BusinessPlanResponse(BaseModel):
    responses: List[AgentResponse]
    status: str

@app.post("/generate-business-plan", response_model=BusinessPlanResponse)
async def generate_business_plan(request: BusinessPlanRequest):
    try:
        # Initialize Google Gemini
        #model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Initialize the LLM with Gemini
        llm = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.7
        )

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load configurations
        with open(os.path.join(current_dir, "crews/businessplan_crew/config/agents.yaml"), "r") as f:
            agents_config = yaml.safe_load(f)
        
        with open(os.path.join(current_dir, "crews/businessplan_crew/config/tasks.yaml"), "r") as f:
            tasks_config = yaml.safe_load(f)

        # Create and run the crew
        crew = BusinessPlanCrew(agents_config, tasks_config, llm)
        result = crew.crew.kickoff(inputs={"business_idea": request.business_concept})
        
        # Collect all agent responses
        responses = []
        for task in crew.tasks:
            responses.append(AgentResponse(
                role=task.agent.role,
                content=task.output.raw if hasattr(task, 'output') else ""
            ))
        
        return BusinessPlanResponse(
            responses=responses,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
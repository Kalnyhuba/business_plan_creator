'''backend.py:

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import LLM
import yaml
from .crews.businessplan_crew.businessplan_crew import BusinessPlanCrew
from .crews.review_business_plan.review_business_plan import ReviewBusinessPlanCrew
from typing import List, Dict, Optional
import os
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class BusinessPlanRequest(BaseModel):
    business_concept: str
    market_input: str
    competition_input: str
    product_input: str
    marketing_input: str
    financial_input: str

class AgentResponse(BaseModel):
    role: str
    content: str

class BusinessPlanResponse(BaseModel):
    responses: List[AgentResponse]
    status: str
    feedback: Optional[str] = None
    valid: bool = False

@app.post("/generate-business-plan", response_model=BusinessPlanResponse)
async def generate_business_plan(request: BusinessPlanRequest):
    try:
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

        with open(os.path.join(current_dir, "crews/review_business_plan/config/agents.yaml"), "r") as f:
            review_agents_config = yaml.safe_load(f)
        
        with open(os.path.join(current_dir, "crews/review_business_plan/config/tasks.yaml"), "r") as f:
            review_tasks_config = yaml.safe_load(f)

        max_retries = 3
        retry_count = 0
        feedback = None
        valid = False

        while retry_count < max_retries and not valid:
            # Create and run the business plan crew
            inputs = {
                "business_concept": request.business_concept,
                "market_input": request.market_input,
                "competition_input": request.competition_input,
                "product_input": request.product_input,
                "marketing_input": request.marketing_input,
                "financial_input": request.financial_input,
                "feedback": feedback
            }
            crew = BusinessPlanCrew(agents_config, tasks_config, llm, inputs=inputs)
            crew.crew.kickoff()
            
            # Collect all agent responses
            responses = []
            for task in crew.tasks:
                task_output = task.output.raw if hasattr(task, 'output') else ""
                responses.append(AgentResponse(
                    role=task.agent.role,
                    content=task_output
                ))

            # Review the generated plan
            review_crew = ReviewBusinessPlanCrew(review_agents_config, review_tasks_config, llm)
            review_result = review_crew.review_plan("\n".join([r.content for r in responses]))
            
            print(f"Review result type: {type(review_result)}")
            print(f"Review result: {review_result}")
            
            # Check if the plan is valid
            if isinstance(review_result, dict):
                valid = review_result.get("valid", False)
                feedback = review_result.get("feedback", "")
                print(f"Parsed valid: {valid}, feedback: {feedback}")
            else:
                valid = False
                feedback = f"Invalid review result format: {str(review_result)}"
                print(f"Invalid result format: {feedback}")
            
            if not valid:
                retry_count += 1
                print(f"Plan not valid. Retry {retry_count}/{max_retries}")
                print(f"Feedback: {feedback}")
            else:
                print("Plan validated successfully!")
                break  # Exit the loop when valid
        
        return BusinessPlanResponse(
            responses=responses,
            status="success" if valid else "failed",
            feedback=feedback,
            valid=valid
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
frontend.py:

import streamlit as st
import requests

st.set_page_config(page_title="Business Plan Creator", page_icon="📊")

st.title("Business Plan Creator")
st.write("Generate a comprehensive business plan using AI")

# Input field for business concept
business_concept = st.text_input("Describe your company briefly, please provide the name of the company, what kind of products/services it offers and the location of the company", placeholder="e.g., A sustainable fashion brand using recycled materials")

market_input = st.text_area("Describe what industry does the company operate in, and possible target markets", placeholder="e.g., Industry, markets")

competition_input = st.text_area("List some competitors on the market and describe the competition in the industry in general", placeholder="e.g., There is high competition in this industry, because...")

product_input = st.text_area("Describe the product or service the company offers. Write about the value proposed by the product or service, its characteristics and how it is built/organised", placeholder="e.g., We propose a revolutionary solution for cooking etc.")

# Input field for marketing expert
marketing_input = st.text_area("Describe how would you expect to attract customers and how would you advertise the company:", placeholder="e.g., Marketing channels, branding strategy, advertisements")

# Input field for financial expert
financial_input = st.text_area("Describe how much are you willing to invest and how do you intend to generate sales and profits for the company:", placeholder="e.g., Initial investment amount, revenue targets, cost structure")

if st.button("Generate Business Plan"):
    if business_concept:
        with st.spinner("Generating your business plan..."):
            try:
                # Call the FastAPI backend
                response = requests.post(
                    "http://localhost:8000/generate-business-plan",
                    json={
                        "business_concept": business_concept,
                        "market_input": market_input,
                        "competition_input": competition_input,
                        "product_input": product_input,
                        "marketing_input": marketing_input,
                        "financial_input": financial_input
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display each agent's response
                    st.markdown("### Generated Business Plan")
                    
                    # Combine all responses for the download
                    full_content = "# Business Plan\n\n"
                    
                    for agent_response in result["responses"]:
                        st.markdown(f"#### {agent_response['role']}")
                        st.markdown(agent_response['content'])
                        st.markdown("---")
                        
                        # Add to full content for download
                        full_content += f"## {agent_response['role']}\n\n"
                        full_content += agent_response['content']
                        full_content += "\n\n---\n\n"
                    
                    # Add download button with full content
                    st.download_button(
                        label="Download Business Plan",
                        data=full_content,
                        file_name="business_plan.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to the server: {str(e)}")
    else:
        st.warning("Please describe your business concept.")'''
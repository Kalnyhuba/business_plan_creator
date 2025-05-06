from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .crews.businessplan_crew.businessplan_crew import BusinessPlanCrew
from .crews.webscraper_crew.webscraper_crew import WebscraperCrew
from typing import List, Dict, Optional, Union, Any, Tuple
import os
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class WebsiteScrapeRequest(BaseModel):
    website_url: str

class WebsiteScrapeResponse(BaseModel):
    scraped_data: str
    status: str

class QuestionAnswer(BaseModel):
    question: str
    answer: Optional[Union[str, List[str], Dict[str, Any], bool, int, None]] = None

class KeyResourcesEvaluation(BaseModel):
    tangible_resources: QuestionAnswer
    intangible_resources: QuestionAnswer
    company_activities: QuestionAnswer
    material_resources: QuestionAnswer
    intangible_resources_selected: QuestionAnswer
    important_activities: QuestionAnswer
    activity_division: QuestionAnswer
    activity_performance: Optional[QuestionAnswer] = None

class StrategicPartnersEvaluation(BaseModel):
    partners_importance: QuestionAnswer
    company_statements: QuestionAnswer
    important_partners: QuestionAnswer
    partnership_benefits: QuestionAnswer
    other_benefit: Optional[QuestionAnswer] = None
    outsourced_activities: Optional[QuestionAnswer] = None
    other_outsourced_activity: Optional[QuestionAnswer] = None
    outsourced_for_brand: Optional[QuestionAnswer] = None

class CostStructureEvaluation(BaseModel):
    cost_intensive_components: QuestionAnswer
    focus_areas: QuestionAnswer

class DigitalizationEvaluation(BaseModel):
    tech_changes_intensity: QuestionAnswer
    used_technologies: QuestionAnswer
    other_technology: Optional[QuestionAnswer] = None
    technology_usage: Optional[QuestionAnswer] = None

class GreenTransformationEvaluation(BaseModel):
    green_transformation: QuestionAnswer
    green_transition_challenges: QuestionAnswer
    green_transition_motivations: QuestionAnswer
    recycling_materials: Optional[QuestionAnswer] = None

class TeamMember(BaseModel):
    name: str
    position: str
    competencies: str
    experience: str

class RiskFactor(BaseModel):
    factor: str
    plan: Optional[str] = None

class FundingStrategy(BaseModel):
    amount: int
    purpose: Optional[str] = None

class BusinessPlanRequest(BaseModel):
    # Basic Information
    has_website: Optional[QuestionAnswer] = None
    website_url: Optional[QuestionAnswer] = None
    scraped_data: Optional[str] = None
    business_name: Optional[QuestionAnswer] = None
    start_year: Optional[QuestionAnswer] = None
    business_reason: Optional[QuestionAnswer] = None
    mission_vision: Optional[QuestionAnswer] = None
    legal_structure: Optional[QuestionAnswer] = None
    financial_funding: Optional[QuestionAnswer] = None
    
    # Business Sector Information
    business_sector: Optional[QuestionAnswer] = None
    raw_materials_type: Optional[QuestionAnswer] = None
    industrial_business_type: Optional[QuestionAnswer] = None
    services_type: Optional[QuestionAnswer] = None
    durable_goods_type: Optional[QuestionAnswer] = None
    consumer_goods_type: Optional[QuestionAnswer] = None
    healtcare_type: Optional[QuestionAnswer] = None
    financial_services_type: Optional[QuestionAnswer] = None
    information_technology_type: Optional[QuestionAnswer] = None
    utilities_type: Optional[QuestionAnswer] = None
    culture_type: Optional[QuestionAnswer] = None
    
    # Market Information
    primary_countries: Optional[QuestionAnswer] = None
    characteristics: Optional[QuestionAnswer] = None
    product_centralisation: Optional[QuestionAnswer] = None
    product_range: Optional[QuestionAnswer] = None
    end_consumer_characteristics: Optional[QuestionAnswer] = None
    end_consumer_characteristics_2: Optional[QuestionAnswer] = None
    
    # Product and Customer Segment Information
    product_service_description: QuestionAnswer
    segment_name: Optional[QuestionAnswer] = None
    segment_demographics: Optional[QuestionAnswer] = None
    segment_characteristics: Optional[QuestionAnswer] = None
    customer_count: Optional[QuestionAnswer] = None
    problems_faced: Optional[QuestionAnswer] = None
    biggest_competitors: Optional[QuestionAnswer] = None
    competition_intensity: Optional[QuestionAnswer] = None
    price_comparison: Optional[QuestionAnswer] = None
    market_type: Optional[QuestionAnswer] = None
    competitive_parameters: Optional[QuestionAnswer] = None
    value_propositions: Optional[QuestionAnswer] = None
    direct_income: Optional[QuestionAnswer] = None
    primary_revenue: Optional[QuestionAnswer] = None
    one_time_payments: Optional[QuestionAnswer] = None
    ongoing_payments: Optional[QuestionAnswer] = None
    payment_characteristics: Optional[QuestionAnswer] = None
    package_price: Optional[QuestionAnswer] = None
    price_negotiation: Optional[QuestionAnswer] = None
    fixed_prices: Optional[QuestionAnswer] = None
    dynamic_prices: Optional[QuestionAnswer] = None
    distribution_channels: Optional[QuestionAnswer] = None
    purchasing_power: Optional[QuestionAnswer] = None
    product_related_characteristics: Optional[QuestionAnswer] = None
    self_service_availability: Optional[QuestionAnswer] = None
    online_communities_presence: Optional[QuestionAnswer] = None
    development_process_customer_involvement: Optional[QuestionAnswer] = None
    after_sale_purchases: Optional[QuestionAnswer] = None
    personal_assistance_offered: Optional[QuestionAnswer] = None
    similar_products_switch: Optional[QuestionAnswer] = None
    general_customer_relation: Optional[QuestionAnswer] = None

    # Key Resources and Strategic Partners Information
    key_resources: Optional[KeyResourcesEvaluation] = None
    strategic_partners: Optional[StrategicPartnersEvaluation] = None

    # Cost Structure and Focus Areas
    cost_structure: Optional[CostStructureEvaluation] = None

    # Digitalization and Green Transformation
    digitalization: Optional[DigitalizationEvaluation] = None
    green_transformation: Optional[GreenTransformationEvaluation] = None

    # Team Information
    team_members: Optional[QuestionAnswer] = None  # Changed to QuestionAnswer type

    # Target Markets and Funding
    target_countries: Optional[QuestionAnswer] = None
    funding_strategy: Optional[QuestionAnswer] = None

class AgentResponse(BaseModel):
    role: str
    content: str

class BusinessPlanResponse(BaseModel):
    responses: List[AgentResponse]
    status: str
    feedback: Optional[str] = None
    valid: bool = False

@app.post("/scrape-website", response_model=WebsiteScrapeResponse)
async def scrape_website(request: WebsiteScrapeRequest):
    try:
        # Create the webscraper crew
        crew = WebscraperCrew()
        
        # Set the website URL
        crew.inputs = {"website_url": request.website_url}
        
        # Run the crew
        result = crew.crew().kickoff()
        
        # Get the scraped data from the result
        scraped_data = result[0].output.raw if result and len(result) > 0 else ""
        
        return WebsiteScrapeResponse(
            scraped_data=scraped_data,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-business-plan", response_model=BusinessPlanResponse)
async def generate_business_plan(request: BusinessPlanRequest):
    try:
        # Create the business plan crew
        crew = BusinessPlanCrew()
        
        # Set the inputs for the crew
        crew.inputs = {
            "business_name": request.business_name,
            "product_service_description": request.product_service_description,
            "target_markets": request.primary_countries,
            "has_website": request.has_website.answer if request.has_website else None,
            "website_url": request.website_url.answer if request.website_url else None,
            "scraped_data": request.scraped_data,
            "start_year": request.start_year.answer if request.start_year else None,
            "business_reason": request.business_reason.answer if request.business_reason else None,
            "mission_vision": request.mission_vision.answer if request.mission_vision else None,
            "legal_structure": request.legal_structure.answer if request.legal_structure else None,
            "financial_funding": request.financial_funding.answer if request.financial_funding else None,
            "business_sector": request.business_sector.answer if request.business_sector else None,
            "sector_specific_type": {
                "raw_materials": request.raw_materials_type.answer if request.raw_materials_type else None,
                "industrial_business": request.industrial_business_type.answer if request.industrial_business_type else None,
                "services": request.services_type.answer if request.services_type else None,
                "durable_goods": request.durable_goods_type.answer if request.durable_goods_type else None,
                "consumer_goods": request.consumer_goods_type.answer if request.consumer_goods_type else None,
                "healthcare": request.healtcare_type.answer if request.healtcare_type else None,
                "financial_services": request.financial_services_type.answer if request.financial_services_type else None,
                "information_technology": request.information_technology_type.answer if request.information_technology_type else None,
                "utilities": request.utilities_type.answer if request.utilities_type else None,
                "culture": request.culture_type.answer if request.culture_type else None
            },
            "characteristics": request.characteristics.answer if request.characteristics else None,
            "product_centralisation": request.product_centralisation.answer if request.product_centralisation else None,
            "product_range": request.product_range.answer if request.product_range else None,
            "end_consumer_characteristics": request.end_consumer_characteristics.answer if request.end_consumer_characteristics else None,
            "end_consumer_characteristics_2": request.end_consumer_characteristics_2.answer if request.end_consumer_characteristics_2 else None,
            # Second page information
            "segment_name": request.segment_name.answer if request.segment_name else None,
            "segment_demographics": request.segment_demographics.answer if request.segment_demographics else None,
            "segment_characteristics": request.segment_characteristics.answer if request.segment_characteristics else None,
            "customer_count": request.customer_count.answer if request.customer_count else None,
            "problems_faced": request.problems_faced.answer if request.problems_faced else None,
            "biggest_competitors": request.biggest_competitors.answer if request.biggest_competitors else None,
            "competition_intensity": request.competition_intensity.answer if request.competition_intensity else None,
            "price_comparison": request.price_comparison.answer if request.price_comparison else None,
            "market_type": request.market_type.answer if request.market_type else None,
            "competitive_parameters": request.competitive_parameters.answer if request.competitive_parameters else None,
            "value_propositions": request.value_propositions.answer if request.value_propositions else None,
            "direct_income": request.direct_income.answer if request.direct_income else None,
            "primary_revenue": request.primary_revenue.answer if request.primary_revenue else None,
            "one_time_payments": request.one_time_payments.answer if request.one_time_payments else None,
            "ongoing_payments": request.ongoing_payments.answer if request.ongoing_payments else None,
            "payment_characteristics": request.payment_characteristics.answer if request.payment_characteristics else None,
            "package_price": request.package_price.answer if request.package_price else None,
            "price_negotiation": request.price_negotiation.answer if request.price_negotiation else None,
            "fixed_prices": request.fixed_prices.answer if request.fixed_prices else None,
            "dynamic_prices": request.dynamic_prices.answer if request.dynamic_prices else None,
            "distribution_channels": request.distribution_channels.answer if request.distribution_channels else None,
            "purchasing_power": request.purchasing_power.answer if request.purchasing_power else None,
            "product_related_characteristics": request.product_related_characteristics.answer if request.product_related_characteristics else None,
            "self_service_availability": request.self_service_availability.answer if request.self_service_availability else None,
            "online_communities_presence": request.online_communities_presence.answer if request.online_communities_presence else None,
            "development_process_customer_involvement": request.development_process_customer_involvement.answer if request.development_process_customer_involvement else None,
            "after_sale_purchases": request.after_sale_purchases.answer if request.after_sale_purchases else None,
            "personal_assistance_offered": request.personal_assistance_offered.answer if request.personal_assistance_offered else None,
            "similar_products_switch": request.similar_products_switch.answer if request.similar_products_switch else None,
            "general_customer_relation": request.general_customer_relation.answer if request.general_customer_relation else None,
            "key_resources": request.key_resources if request.key_resources else None,
            "strategic_partners": request.strategic_partners if request.strategic_partners else None,
            "cost_structure": request.cost_structure if request.cost_structure else None,
            "digitalization": request.digitalization if request.digitalization else None,
            "green_transformation": request.green_transformation if request.green_transformation else None,
            "team_members": request.team_members if request.team_members else None,
            "target_countries": request.target_countries.answer if request.target_countries else None,
            "funding_strategy": request.funding_strategy if request.funding_strategy else None
        }
        
        # Run the crew
        crew.crew().kickoff()
        
        # Collect all agent responses
        responses = []
        for task in crew.tasks:
            task_output = task.output.raw if hasattr(task, 'output') else ""
            responses.append(AgentResponse(
                role=task.agent.role,
                content=task_output
            ))
        
        return BusinessPlanResponse(
            responses=responses,
            status="success",
            valid=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
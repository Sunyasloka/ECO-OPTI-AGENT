# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.4,google_api_key=os.getenv("GOOGLE_API_KEY"))

# prompt_template = PromptTemplate(
#     input_variables=["uses_diesel_generator", "uses_lpg_or_propane"],
#     template="""
# You are a carbon footprint analyst.

# Given the inputs:
# - Uses Diesel Generator: {uses_diesel_generator}
# - Uses LPG/Propane: {uses_lpg_or_propane}

# Your tasks:
# 1. Estimate approximate monthly CO₂ emissions from:
#    - Diesel generators (assume 2.7 kg CO₂ per liter, average 5 liters/day if used)
#    - LPG/Propane usage (assume 2.9 kg CO₂ per kg, average 30 kg/month if used)

# 2. Suggest alternatives or optimizations (e.g., solar backup, electric appliances, battery systems)

# Output format:
# - Estimated CO₂ Emission (kg/month): ___
# - Suggestions: [bullet points]
# """
# )

# def run_fuel_agent(inputs: dict) -> dict:
#     try:
#         uses_diesel_generator = inputs.get("uses_diesel_generator", False)
#         uses_lpg_or_propane = inputs.get("uses_lpg_or_propane", False)

#         prompt = prompt_template.format(
#             uses_diesel_generator=uses_diesel_generator,
#             uses_lpg_or_propane=uses_lpg_or_propane
#         )

#         response = llm.invoke(prompt)

#         return {
#             "agent": "FuelAgent",
#             "output": response.content
#         }

#     except Exception as e:
#         return {
#             "agent": "FuelAgent",
#             "error": str(e)
#         }
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class FuelSuggestions(BaseModel):
    suggestions: list[str] = Field(..., description="A list of three actionable suggestions for reducing emissions from fuel usage.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))
llm_with_structure = llm.with_structured_output(FuelSuggestions)

def calculate_fuel_emissions(uses_diesel, uses_lpg):
    diesel_emission_factor = 2.7
    lpg_emission_factor = 2.9
    total_emissions = 0
    if uses_diesel:
        total_emissions += 5 * 30 * diesel_emission_factor
    if uses_lpg:
        total_emissions += 30 * lpg_emission_factor
    return round(total_emissions, 2)

prompt_template = PromptTemplate(
    input_variables=["uses_diesel_generator", "uses_lpg_or_propane", "fuel_emission_kg_per_month"],
    template="""
You are a carbon footprint analyst.
Given the inputs:
- Uses Diesel Generator: {uses_diesel_generator}
- Uses LPG/Propane: {uses_lpg_or_propane}
The estimated approximate monthly CO₂ emissions from fuel usage is {fuel_emission_kg_per_month} kg/month.

Provide exactly three actionable suggestions to reduce these emissions. Do not include any other text or explanation.
"""
)

def run_fuel_agent(inputs: dict) -> tuple:
    try:
        uses_diesel_generator = inputs.get("uses_diesel_generator", False)
        uses_lpg_or_propane = inputs.get("uses_lpg_or_propane", False)
        fuel_emission_kg_per_month = calculate_fuel_emissions(uses_diesel_generator, uses_lpg_or_propane)

        inputs["fuel_emission_kg_per_month"] = fuel_emission_kg_per_month
        chain = prompt_template | llm_with_structure
        response = chain.invoke(inputs)
        
        return response.suggestions, fuel_emission_kg_per_month

    except Exception as e:
        print(f"Error in Fuel Agent: {e}")
        return (["No suggestions available due to error."], 0)
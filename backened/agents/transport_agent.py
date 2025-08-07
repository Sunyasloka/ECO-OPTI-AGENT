# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain_core.prompts import PromptTemplate
# # from dotenv import load_dotenv
# # import os

# # load_dotenv()

# # llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.4,google_api_key=os.getenv("GOOGLE_API_KEY"))

# # prompt_template = PromptTemplate(
# #     input_variables=["number_of_diesel_vehicles", "avg_km_per_vehicle_per_day"],
# #     template="""
# # You are a sustainability expert.

# # Based on the following data:
# # - Number of diesel vehicles: {number_of_diesel_vehicles}
# # - Average km driven per vehicle per day: {avg_km_per_vehicle_per_day}

# # 1. Calculate total CO₂ emissions per month (assume 2.68 kg CO₂ per liter of diesel and 12 km per liter mileage).
# # 2. Suggest practical optimizations to reduce transport-related emissions (e.g., switching to EVs, optimizing routes, carpooling, telecommuting, etc).
# # 3. Present your output in this format:
# #     - Estimated CO₂ Emission (kg/month): ___
# #     - Optimization Suggestions: [bullet list]
# # """
# # )

# # def run_transport_agent(inputs: dict) -> dict:
# #     try:
# #         number_of_diesel_vehicles = inputs.get("number_of_diesel_vehicles", 0)
# #         avg_km_per_vehicle_per_day = inputs.get("average_km_per_vehicle_per_day", 0)

# #         prompt = prompt_template.format(
# #             number_of_diesel_vehicles=number_of_diesel_vehicles,
# #             avg_km_per_vehicle_per_day=avg_km_per_vehicle_per_day
# #         )

# #         response = llm.invoke(prompt)

# #         return {
# #             "agent": "TransportAgent",
# #             "output": response.content
# #         }
# #     except Exception as e:
# #         return {
# #         
# #     "agent": "TransportAgent",
# #             "error": str(e)
# #         }
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from pydantic import BaseModel, Field
# from dotenv import load_dotenv
# import os

# load_dotenv()

# class TransportSuggestions(BaseModel):
#     suggestions: list[str] = Field(..., description="A list of three actionable suggestions for reducing transport-related emissions.")

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))
# llm_with_structure = llm.with_structured_output(TransportSuggestions)

# def calculate_transport_emissions(num_vehicles, avg_km_per_day):
#     if num_vehicles == 0 or avg_km_per_day == 0:
#         return 0
#     liters_per_day = (num_vehicles * avg_km_per_day) / 12
#     emissions_kg_per_day = liters_per_day * 2.68
#     return round(emissions_kg_per_day * 30, 2)

# prompt_template = PromptTemplate(
#     input_variables={"number_of_diesel_vehicles", "average_km_per_vehicle_per_day", "transport_emission_kg_per_month"},
#     template="""
# You are a sustainability expert.
# Based on the following data:
# - Number of diesel vehicles: {number_of_diesel_vehicles}
# - Average km driven per vehicle per day: {avg_km_per_vehicle_per_day}
# The total CO₂ emissions per month is estimated to be {transport_emission_kg_per_month} kg.

# Provide exactly three actionable suggestions to reduce transport-related emissions. Do not include any other text or explanation.
# """
# )

# def run_transport_agent(inputs: dict) -> tuple:
#     try:
#         number_of_diesel_vehicles = inputs.get("number_of_diesel_vehicles", 0)
#         avg_km_per_vehicle_per_day = inputs.get("average_km_per_vehicle_per_day", 0)
#         transport_emission_kg_per_month = calculate_transport_emissions(number_of_diesel_vehicles, avg_km_per_vehicle_per_day)

#         inputs["transport_emission_kg_per_month"] = transport_emission_kg_per_month
#         chain = prompt_template | llm_with_structure
#         response = chain.invoke(inputs)

#         return response.suggestions, transport_emission_kg_per_month

#     except Exception as e:
#         print(f"Error in Transport Agent: {e}")
#         return (["No suggestions available due to error."], 0)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class TransportSuggestions(BaseModel):
    suggestions: list[str] = Field(..., description="A list of three actionable suggestions for reducing transport-related emissions.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))
llm_with_structure = llm.with_structured_output(TransportSuggestions)

def calculate_transport_emissions(num_vehicles, avg_km_per_day):
    if num_vehicles == 0 or avg_km_per_day == 0:
        return 0
    liters_per_day = (num_vehicles * avg_km_per_day) / 12
    emissions_kg_per_day = liters_per_day * 2.68
    return round(emissions_kg_per_day * 30, 2)

prompt_template = PromptTemplate(
    input_variables={"number_of_diesel_vehicles", "average_km_per_vehicle_per_day", "transport_emission_kg_per_month"},
    template="""
You are a sustainability expert.
Based on the following data:
- Number of diesel vehicles: {number_of_diesel_vehicles}
- Average km driven per vehicle per day: {average_km_per_vehicle_per_day}
The total CO₂ emissions per month is estimated to be {transport_emission_kg_per_month} kg.

Provide exactly three actionable suggestions to reduce transport-related emissions. Do not include any other text or explanation.
"""
)

def run_transport_agent(inputs: dict) -> tuple:
    try:
        number_of_diesel_vehicles = inputs.get("number_of_diesel_vehicles", 0)
        avg_km_per_vehicle_per_day = inputs.get("average_km_per_vehicle_per_day", 0)
        transport_emission_kg_per_month = calculate_transport_emissions(number_of_diesel_vehicles, avg_km_per_vehicle_per_day)

        inputs["transport_emission_kg_per_month"] = transport_emission_kg_per_month
        chain = prompt_template | llm_with_structure
        response = chain.invoke(inputs)

        return response.suggestions, transport_emission_kg_per_month

    except Exception as e:
        print(f"Error in Transport Agent: {e}")
        return (["No suggestions available due to error."], 0)
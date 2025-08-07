from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class ElectricitySuggestions(BaseModel):
    suggestions: list[str] = Field(..., description="A list of three actionable suggestions for reducing electricity consumption.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=os.getenv("GOOGLE_API_KEY"))
llm_with_structure = llm.with_structured_output(ElectricitySuggestions)

electricity_prompt = PromptTemplate(
    input_variables=[
        "lighting_type", "light_usage_hours_per_day", "number_of_ac_units",
        "ac_usage_hours_per_day", "monthly_electricity_bill", "uses_solar_panels",
        "uses_energy_efficient_devices", "estimated_co2_emission"
    ],
    template="""
You are an energy optimization assistant.
The user provides:
- Lighting type: {lighting_type}
- Light usage hours/day: {light_usage_hours_per_day}
- AC units: {number_of_ac_units}
- AC usage hours/day: {ac_usage_hours_per_day}
- Monthly electricity bill: ₹{monthly_electricity_bill}
- Uses solar panels: {uses_solar_panels}
- Uses energy efficient devices: {uses_energy_efficient_devices}
The estimated electricity CO2 emission is {estimated_co2_emission} kg/month.

Provide exactly three actionable suggestions to optimize energy usage and reduce this emission. Do not include any other text or explanation.
"""
)

def run_electricity_agent(input_data):
    LED_WATTAGE = 10
    AC_WATTAGE_KW = 1.5
    num_lights = 10
    light_usage_hours = input_data.get("light_usage_hours_per_day", 0)
    ac_units = input_data.get("number_of_ac_units", 0)
    ac_usage_hours = input_data.get("ac_usage_hours_per_day", 0)
    
    monthly_kwh_lights = (num_lights * LED_WATTAGE * light_usage_hours * 30) / 1000
    monthly_kwh_ac = (ac_units * AC_WATTAGE_KW * ac_usage_hours * 30)
    total_kwh_monthly = monthly_kwh_lights + monthly_kwh_ac
    
    electricity_emission = round(total_kwh_monthly * 0.82, 2)
    input_data["estimated_co2_emission"] = electricity_emission
    
    try:
        chain = electricity_prompt | llm_with_structure
        response = chain.invoke(input_data)
        
        if response:
            return response.suggestions, electricity_emission
        else:
            print("Warning: LLM returned an empty response for electricity_agent.")
            return ["No suggestions available due to an empty LLM response."], electricity_emission
            
    except Exception as e:
        print(f"Error in Electricity Agent: {e}")
        return ["No suggestions available due to an error."], electricity_emission
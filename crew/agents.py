from crewai import Agent, LLM
from crew.tools import GeoLocationTool, WeatherTool
import os
from dotenv import load_dotenv

load_dotenv()

class Agents:
    def meteorologista(self):

        llm = LLM(
            model=os.getenv("OPENAI_MODEL_NAME"),
            api_key=os.getenv("OPENAI_API_KEY")
        )

        return Agent(
            role='Meteorologista',
            goal='Informar sobre o clima de determinado lugar',
            backstory="""Especialista em informar sobre o clima de determinado lugar.""",
            verbose=True,
            allow_delegation=False,
            tools=[GeoLocationTool(), WeatherTool()],
            llm=llm
        )

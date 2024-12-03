from crewai.tools import BaseTool
import requests

class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Use this tool to get the weather in a given location."

    def _run(self, latitude: float, longitude: float) -> str:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=apparent_temperature,wind_speed_10m")
        if response.status_code != 200:
            return "Erro ao obter o clima."
        data = response.json()
        temperature = data["current"]["apparent_temperature"]
        wind_speed = data["current"]["wind_speed_10m"]
        return f"A temperatura é de {temperature} com ventos de {wind_speed}."

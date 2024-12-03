from crewai.tools import BaseTool
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GeoLocationTool(BaseTool):

    name:str = "GeoLocation Tool"
    description:str = "Use this tool to get the coordinates of a given location."
    
    def _run(self, city_name: str) -> str:
        api_key = os.getenv("OPENCAGE_API_KEY")  # Substitua pela sua chave de API do OpenCage
        base_url = "https://api.opencagedata.com/geocode/v1/json"
        
        params = {
            "q": city_name,
            "key": api_key,
            "language": "pt",  # Idioma da resposta
            "pretty": 1        # Formata a resposta para melhor leitura (opcional)
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                latitude = data['results'][0]['geometry']['lat']
                longitude = data['results'][0]['geometry']['lng']
                return f"Latitude: {latitude}, Longitude: {longitude}"  # "latitude, longitude
            else:
                return 'Nenhum resultado encontrado.'
        else:
            print("Erro ao acessar a API:", response.status_code)
            return None
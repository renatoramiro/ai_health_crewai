from crewai import Task

class Tasks:
    def informar_clima(self, agent, location, history=None):
        history_text = f"\nUtilize o chat history para obter informações:\n{history}" if history else ""
        
        return Task(
            description=f"""
            {history_text}

            Use a ferramenta geolocation_tool, que receberá o nome de uma {location}, informe a latitude e longitude da mesma.
            Use a ferramenta weather_tool, que receberá a latitude e longitude de uma {location}, informe o clima da mesma.
            Com as informações do clima, informe ao usuário o clima em {location}. A temperatura sempre é em Celsius (°C) e a velocidade do vento em km/h.
            """,
            agent=agent,
            expected_output="Uma frase informando o clima em {location}."
        )

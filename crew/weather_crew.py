from crewai import Crew
from .agents import Agents
from .tasks import Tasks

class WeatherCrew:
    def __init__(self):
        print("Inicializando WeatherCrew...")
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, message, sender, history):        
        print(f"WeatherCrew.run - Mensagem: {message}, Sender: {sender}")
        print(f"Histórico disponível: {history}")
        
        # Initialize agents
        print("Inicializando agente meteorologista...")
        meteorologista = self.agents.meteorologista()

        # Create tasks
        print("Criando task informar_clima...")
        informar_clima = self.tasks.informar_clima(
            meteorologista, 
            message,
            history=history
        )

        # Create crew
        print("Configurando crew...")
        crew = Crew(
            agents=[meteorologista],
            tasks=[informar_clima],
            verbose=True,
        )

        # Execute the workflow
        print("Iniciando execução do workflow...")
        try:
            result = crew.kickoff(inputs={"location": message})
            print(f"Workflow concluído. Resultado: {result}")
            return result
        except Exception as e:
            print(f"Erro durante execução do workflow: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise

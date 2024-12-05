from crewai import Crew, Process
from .agents import Agents
from .tasks import Tasks

import os
from dotenv import load_dotenv

load_dotenv()

class EntrevistadorCrew:
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, message, history=None):
        print("Iniciando o fluxo de entrevistador...")
        
        # Initialize agents
        print("Inicializando agente 'entrevistador'...")
        entrevistador = self.agents.entrevistador()

        # Create entrevistador task
        print("Criando task 'obter_informacoes_paciente'...")
        obter_informacoes_paciente = self.tasks.obter_informacoes_paciente(
            entrevistador,
            message,
            history=history
        )

        # Create entrevistador crew
        print("Criando crew do entrevistador...")
        entrevistador_crew = Crew(
            agents=[entrevistador],
            tasks=[obter_informacoes_paciente],
            verbose=True
        )

        # Run entrevistador crew
        print("Executando crew do entrevistador...")
        return entrevistador_crew.kickoff()
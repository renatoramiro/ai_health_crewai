from crewai import Crew, Process
from .agents import Agents
from .tasks import Tasks

import os
from dotenv import load_dotenv

load_dotenv()

class ManagerCrew:
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, message, history=None):
        print("Iniciando o fluxo de gerente de trabalho...")
        
        # Initialize agents
        print("Inicializando agente 'manager'...")
        manager = self.agents.manager()

        # Create manager task to check information completeness
        print("Criando task 'gerenciar'...")
        gerenciar = self.tasks.gerenciar(
            manager,
            message,
            history=history
        )

        # Create manager crew
        print("Criando crew do manager...")
        manager_crew = Crew(
            agents=[manager],
            tasks=[gerenciar],
            verbose=True
        )

        # Run manager crew
        print("Executando crew do manager...")
        return manager_crew.kickoff()
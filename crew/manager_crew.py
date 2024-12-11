from crewai import Crew
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
        # Initialize agents
        manager = self.agents.manager()

        # Create manager task to check information completeness
        gerenciar = self.tasks.gerenciar(
            manager,
            message,
            history=history
        )

        # Create manager crew
        manager_crew = Crew(
            agents=[manager],
            tasks=[gerenciar],
            verbose=True
        )

        # Run manager crew
        result = manager_crew.kickoff({'history': history})
        print('Resultado do ManagerCrew:', result)
        return result
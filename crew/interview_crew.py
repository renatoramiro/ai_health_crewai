from crewai import Crew, Process
from .agents import Agents
from .tasks import Tasks

import os
from dotenv import load_dotenv

load_dotenv()

class InterviewCrew:
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, message, history=None):
        # Initialize agents
        entrevistador = self.agents.entrevistador()

        # Create entrevistador task
        obter_informacoes_paciente = self.tasks.obter_informacoes_paciente(
            entrevistador,
            history=history
        )

        # Create entrevistador crew
        entrevistador_crew = Crew(
            agents=[entrevistador],
            tasks=[obter_informacoes_paciente],
            verbose=True
        )

        # Run entrevistador crew
        return entrevistador_crew.kickoff({'history': history})
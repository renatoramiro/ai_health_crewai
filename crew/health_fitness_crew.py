from crewai import Crew, Process
from .agents import Agents
from .tasks import Tasks

import os
from dotenv import load_dotenv

load_dotenv()

class HealthFitnessCrew:
    def __init__(self):
        print("Inicializando HealthFitnessCrew...")
        self.agents = Agents()
        self.tasks = Tasks()
    
    def run(self, history=None):
        print("Iniciando o fluxo de trabalho...")
        
        # Initialize agents
        print("Inicializando agentes...")
        nutricionista = self.agents.nutricionista()
        personal_trainer = self.agents.personal_trainer()
        redator = self.agents.redator()
        enviador_de_email = self.agents.enviador_de_email()
        
        print("Informações completas. Executando o fluxo completo...")
        print("Criando task criar_dieta_personalizada...")
        criar_dieta_personalizada = self.tasks.criar_dieta_personalizada(
            nutricionista,
            history=history
        )

        print("Criando task criar_treino_personalizado...")
        criar_treino_personalizado = self.tasks.criar_treino_personalizado(
            personal_trainer,
            history=history
        )

        print("Criando task escrever_relatorio...")
        escrever_relatorio = self.tasks.escrever_relatorio(
            redator,
            history=history
        )

        print("Criando task enviar_email...")
        enviar_email = self.tasks.enviar_email(
            enviador_de_email,
            history=history
        )

        # Create and run the full workflow
        crew_full = Crew(
            agents=[nutricionista, personal_trainer, redator, enviador_de_email],
            tasks=[criar_dieta_personalizada, criar_treino_personalizado, escrever_relatorio, enviar_email],
            verbose=True
        )

        return crew_full.kickoff({'history': history})

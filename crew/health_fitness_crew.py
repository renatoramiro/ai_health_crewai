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
    
    def run(self, message, history=None):
        print("Iniciando o fluxo de trabalho...")
        
        # Initialize agents
        print("Inicializando agentes...")
        manager = self.agents.manager()
        entrevistador = self.agents.entrevistador()
        nutricionista = self.agents.nutricionista()
        personal_trainer = self.agents.personal_trainer()
        redator = self.agents.redator()

        # Create manager task to check information completeness
        print("Criando task gerenciar...")
        gerenciar = self.tasks.gerenciar(
            manager,
            message,
            history=history
        )

        # Create interview task
        print("Criando task obter_informacoes_paciente...")
        obter_informacoes_paciente = self.tasks.obter_informacoes_paciente(
            entrevistador,
            message,
            history=history
        )

        # First, check if we have all required information
        crew_check = Crew(
            agents=[manager],
            tasks=[gerenciar],
            verbose=True
        )
        
        result = crew_check.kickoff()
        
        # If we don't have all information, only run the interview task
        if str(result) == "False":
            print("Informações incompletas. Executando apenas a entrevista...")
            crew_interview = Crew(
                agents=[entrevistador],
                tasks=[obter_informacoes_paciente],
                verbose=True
            )
            return crew_interview.kickoff()
        else:
            # If we have all information, proceed with the full workflow
            print("Informações completas. Executando o fluxo completo...")
            print("Criando task criar_dieta_personalizada...")
            criar_dieta_personalizada = self.tasks.criar_dieta_personalizada(
                nutricionista,
                message,
                history=history
            )

            print("Criando task criar_treino_personalizado...")
            criar_treino_personalizado = self.tasks.criar_treino_personalizado(
                personal_trainer,
                message,
                history=history
            )

            print("Criando task escrever_relatorio...")
            escrever_relatorio = self.tasks.escrever_relatorio(
                redator,
                message,
                history=history
            )

            # Create and run the full workflow
            crew_full = Crew(
                agents=[entrevistador, nutricionista, personal_trainer, redator],
                tasks=[obter_informacoes_paciente, criar_dieta_personalizada, criar_treino_personalizado, escrever_relatorio],
                verbose=True
            )

            return crew_full.kickoff()

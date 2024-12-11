from crewai import Agent, LLM
import os
from dotenv import load_dotenv
from .tools.send_email_tool import SendEmailTool

load_dotenv()

class Agents:
    def __init__(self):
        self.llm = LLM(
            model=os.getenv("OPENAI_MODEL_NAME"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.llm_man_int = LLM(
            model=os.getenv("OPENAI_MODEL_NAME"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.2
        )

    def manager(self):

        return Agent(
            role='Manager',
            goal='Coordenar o trabalho dos agentes',
            backstory="""Especialista em coordenar e gerenciar o trabalho dos agentes.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm_man_int
        )

    def entrevistador(self):

        return Agent(
            role='Entrevistador',
            goal='Obter TODAS as informações básicas do paciente, como: nome, sexo, idade, peso, altura, atividade fisica e preferências alimentares',
            backstory="""Especialista em escutar e obter informações do paciente.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_man_int
        )

    def nutricionista(self):

        return Agent(
            role='Nutricionista',
            goal='Fornecer informações nutricionais personalizadas',
            backstory="""Especialista experiente em desenvolver dietas personalizadas.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def personal_trainer(self):

        return Agent(
            role='Personal Trainer',
            goal='Fornecer treinos personalizados para o dia-a-dia',
            backstory="""Especialista experiente em desenvolver treinos personalizados para atletas de alto desempenho.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def redator(self):

        return Agent(
            role='Redator',
            goal='Escrever o relatório final com a dieta e o treino personalizado',
            backstory="""Especialista em escrita de dietas e treinos personalizados.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def enviador_de_email(self):

        return Agent(
            role='Enviador de Email',
            goal='Enviar o relatório final por email para o paciente',
            backstory="""Especialista em envio de emails.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[SendEmailTool()]
        )

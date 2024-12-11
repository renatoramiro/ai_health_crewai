from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from .manager_crew import ManagerCrew
from .health_fitness_crew import HealthFitnessCrew
from .interview_crew import InterviewCrew
import json

load_dotenv()

class HistoryState(BaseModel):
    message: str = ''
    history: str = ''
    result: str = ''

class HealthFlow(Flow[HistoryState]):
    @start()
    def etapa_inicial(self):
        print('Inciando o fluxo estruturado...')

    @listen(etapa_inicial)
    def verificar_dados_paciente(self):
        print('Verificando dados do paciente...')
        result = ManagerCrew().run(self.state.message, history=self.state.history)
        self.state.result = result

    @router(verificar_dados_paciente)
    def rotear(self):
        print('Roteando com base nas informações do paciente...')
        try:
            # Limpa a string do resultado para remover marcações markdown
            result_str = str(self.state.result)
            if "```json" in result_str:
                result_str = result_str.split("```json")[-1]
            if "```" in result_str:
                result_str = result_str.split("```")[0]
            result_str = result_str.strip()
            
            print("JSON a ser processado:", result_str)
            
            # Converte o resultado para objeto Python
            dados_paciente = json.loads(result_str)
            
            # Verifica se todas as informações foram fornecidas
            if dados_paciente.get('completo', False):
                print('Todas as informações foram fornecidas')
                return 'sucesso'
            else:
                print('Informações incompletas, continuando entrevista')
                # Log das informações que faltam para debug
                dados = dados_paciente.get('dados', {})
                faltando = [k for k, v in dados.items() if v is None]
                print(f'Informações faltantes: {", ".join(faltando)}')
                return 'falha'
        except json.JSONDecodeError as e:
            print(f'Erro ao decodificar JSON: {e}')
            print(f'String que causou o erro: "{result_str}"')
            return 'falha'
        except Exception as e:
            print(f'Erro inesperado: {e}')
            return 'falha'

    @listen('sucesso')
    def gerar_dieta_exercicio(self):
        print('Gerando dieta e exercícios...')
        result = HealthFitnessCrew().run(self.state.history)
        return result
        # return 'Gerando dieta e exercícios...'

    @listen('falha')
    def entrevistar_paciente(self) -> str:
        print('Entrevistando paciente...')
        result = InterviewCrew().run(self.state.message, history=self.state.history)
        return str(result)

    def run(self, message, history=None):
        return self.kickoff({'message': message, 'history': history})

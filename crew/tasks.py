from crewai import Task

class Tasks:

    def gerenciar(self, agent, message, history=None):
        return Task(
            description=f"""
            Sua tarefa é analisar o histórico da conversa e verificar se o paciente já informou todas as suas informações básicas.

            Histórico da conversa:
            {history}

            Você deve verificar se as seguintes informações já foram EXPLICITAMENTE fornecidas pelo paciente no histórico:
            1. Nome
            2. Sexo
            3. Idade
            4. Peso
            5. Altura
            6. Nível de atividade
            7. Preferências alimentares
            8. Objetivo

            IMPORTANTE:
            - NÃO invente ou assuma informações
            - Só considere informações que foram explicitamente fornecidas pelo paciente
            - Retorne APENAS "True" se TODAS as informações acima foram fornecidas, caso contrário retorne "False"
            """,
            agent=agent,
            expected_output="Retorne APENAS 'True' se todas as informações foram fornecidas pelo paciente, ou 'False' caso contrário."
        )

    def obter_informacoes_paciente(self, agent, message, history=None):
        history_text = f"\nHistórico da conversa:\n{history}" if history else ""
        
        return Task(
            description=f"""
            {history_text}

            Sua tarefa é obter informações básicas sobre o paciente através de perguntas.

            REGRAS IMPORTANTES:
            1. Faça APENAS UMA pergunta por vez
            2. Espere a resposta do paciente antes de fazer a próxima pergunta
            3. NÃO invente ou assuma nenhuma informação
            4. Seja educado e profissional
            5. Mantenha um registro das informações já obtidas
            6. Fale apenas em português do Brasil
            7. NÂO seja prolixo em suas respostas

            Informações necessárias:
            - Nome
            - Sexo
            - Idade
            - Peso
            - Altura
            - Nível de atividade física. Informe as opções: Sedentário, Levemente ativo, Moderadamente ativo, Muito ativo, Extremamente ativo
            - Preferências alimentares. Informe as opções: Vegetariano, Vegano, Dieta de baixo carboidrato, Dieta de baixo gordura, Dieta de baixo gordura e baixo carboidrato, Ceto, Sem glúten, Baixo teor de carboidratos, Sem laticínios, Rico em proteínas.
            - Objetivo. Informe as opções: Perder peso, Ganhar músculos, Resistência, Ficar em forma, Treinamento de força


            EXEMPLO DE INTERAÇÃO:
            Agente: "Olá! Para começar, poderia me dizer seu nome completo?"
            Paciente: "João Silva"
            Agente: "Obrigado João! Qual é a sua idade?"
            
            Se a mensagem for uma saudação ou não contiver informações específicas, comece perguntando o nome.
            Se já tiver algumas informações no histórico, continue de onde parou.
            """,
            agent=agent,
            expected_output="""
            Faça apenas uma pergunta por vez para obter a próxima informação necessária.
            Não retorne um JSON ou lista de informações.
            Apenas faça a próxima pergunta necessária de forma educada e profissional.
            """
        )

    def criar_dieta_personalizada(self, agent, message, history=None):
        history_text = f"\nUtilize o chat history para obter informações:\n{history}" if history else ""
        
        return Task(
            description=f"""
            {history_text}

            Sua tarefa é criar uma dieta personalizada para o paciente com base nas informações fornecidas.

            Você deve:
            1. Analisar o perfil do paciente
            2. Calcular as necessidades calóricas
            3. Distribuir os macronutrientes
            4. Criar um cardápio semanal detalhado
            5. Incluir dicas e recomendações

            Lembre-se de considerar:
            - Preferências alimentares
            - Restrições alimentares
            - Objetivo (perda de peso, ganho de massa, etc)
            - Nível de atividade física
            """,
            agent=agent,
            expected_output="""
            A saída esperada deve ser um texto detalhado que descreve a dieta personalizada, incluindo:
            - Calorias diárias
            - Distribuição de macronutrientes
            - Cardápio semanal
            - Dicas e recomendações
            """
        )

    def criar_treino_personalizado(self, agent, message, history=None):
        history_text = f"\nUtilize o chat history para obter informações:\n{history}" if history else ""
        
        return Task(
            description=f"""
            {history_text}

            Sua tarefa é criar um treino personalizado para o paciente com base nas informações fornecidas.

            Você deve:
            1. Analisar o perfil do paciente
            2. Definir a frequência dos treinos
            3. Selecionar os exercícios apropriados
            4. Especificar séries, repetições e cargas
            5. Incluir orientações técnicas

            Lembre-se de considerar:
            - Nível de condicionamento atual
            - Objetivo (perda de peso, ganho de massa, etc)
            - Limitações físicas
            - Preferências de treino
            """,
            agent=agent,
            expected_output="""
            A saída esperada deve ser um texto detalhado que descreve o treino personalizado, incluindo:
            - Frequência semanal
            - Divisão dos treinos
            - Exercícios detalhados
            - Orientações técnicas
            """
        )

    def escrever_relatorio(self, agent, message, history=None):
        history_text = f"\nUtilize o chat history para obter informações:\n{history}" if history else ""
        
        return Task(
            description=f"""
            {history_text}

            Sua tarefa é escrever um relatório completo e bem formatado que combine a dieta e o treino personalizado.

            Você deve:
            1. Organizar as informações de forma clara e estruturada
            2. Usar formatação markdown para melhor legibilidade
            3. Incluir todas as informações importantes da dieta e do treino
            4. Adicionar observações e recomendações gerais

            O relatório deve incluir:
            - Resumo do perfil do paciente
            - Plano alimentar detalhado
            - Programa de treino completo
            - Dicas e orientações gerais
            """,
            agent=agent,
            expected_output="""
            A saída esperada deve ser um texto em markdown, bem formatado e detalhado que descreve:
            - Perfil completo do paciente
            - Dieta personalizada
            - Treino personalizado
            - Recomendações gerais
            """
        )

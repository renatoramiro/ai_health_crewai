from crewai import Task

class Tasks:

    def gerenciar(self, agent, message, history=None):
        return Task(
            description=f"""
            Sua tarefa é analisar o histórico da conversa e extrair as informações do paciente, verificando se todas as informações básicas já foram fornecidas.

            Histórico da conversa:
            {history}

            INSTRUÇÕES:
            1. Analise cuidadosamente o histórico da conversa
            2. Extraia APENAS informações que foram EXPLICITAMENTE fornecidas pelo paciente
            3. Para cada informação encontrada, registre exatamente como foi informada
            4. NÃO faça suposições ou inferências
            5. Mantenha um registro organizado das informações encontradas

            Informações a serem extraídas e verificadas:
            1. Nome: [extrair do histórico]
            2. Sexo: [extrair do histórico]
            3. Idade: [extrair do histórico]
            4. Peso: [extrair do histórico]
            5. Altura: [extrair do histórico]
            6. Nível de atividade: [extrair do histórico]
            7. Preferências alimentares: [extrair do histórico]
            8. Objetivo: [extrair do histórico]
            9. Email: [extrair do histórico]

            REGRAS IMPORTANTES:
            Retorne as informações no seguinte formato JSON (mantenha exatamente esta estrutura):

            {{{{
                "completo": true,  // Deve ser true se TODOS os campos em "dados" tiverem valores diferentes de null
                "dados": {{{{
                    "nome": "valor ou null",
                    "sexo": "valor ou null",
                    "idade": "valor ou null",
                    "peso": "valor ou null",
                    "altura": "valor ou null",
                    "nivel_atividade": "valor ou null",
                    "preferencias_alimentares": "valor ou null",
                    "objetivo": "valor ou null",
                    "email": "valor ou null"
                }}}}
            }}}}

            IMPORTANTE:
            - Use null quando a informação não foi fornecida
            - Mantenha os valores exatamente como foram informados pelo paciente
            - NÃO faça conversões ou normalizações dos valores
            - O campo "completo" deve ser true APENAS se TODOS os campos em "dados" tiverem valores diferentes de null
            - Se qualquer campo for null, "completo" deve ser false
            """,
            agent=agent,
            expected_output="Retorne um JSON com as informações extraídas do histórico e um indicador se todas as informações foram fornecidas."
        )

    def obter_informacoes_paciente(self, agent, history=None):
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
            - Nível de atividade física. Informe as opções em formato de bullet points: Sedentário, Levemente ativo, Moderadamente ativo, Muito ativo, Extremamente ativo
            - Preferências alimentares. Informe as opções em formato de bullet points: Vegetariano, Vegano, Dieta de baixo carboidrato, Dieta de baixo gordura, Dieta de baixo gordura e baixo carboidrato, Ceto, Sem glúten, Baixo teor de carboidratos, Sem laticínios, Rico em proteínas.
            - Objetivo. Informe as opções em formato de bullet points: Perder peso, Ganhar músculos, Resistência, Ficar em forma, Treinamento de força
            - Email
            
            Se o histórico estiver vazio, pergunte o que o paciente deseja saber.
            Siga a sequencia de perguntas que está em <sequencia_de_perguntas>
            Se já tiver algumas informações no histórico, continue de onde parou.

            <sequencia_de_perguntas>
            1. Qual é o seu nome?
            2. Qual é o seu sexo?
            3. Qual é a sua idade?
            4. Qual é o seu peso?
            5. Qual é a sua altura?
            6. Qual é o seu nível de atividade física?
            7. Qual é suas preferências alimentares?
            8. Qual é o seu objetivo?
            9. Qual é o seu email para que eu possa enviar seu plano de dieta e exercícios?
            </sequencia_de_perguntas>
            """,
            agent=agent,
            expected_output="""
            Faça apenas uma pergunta por vez para obter a próxima informação necessária.
            Não retorne um JSON ou lista de informações.
            Apenas faça a próxima pergunta necessária de forma educada e profissional.
            """
        )

    def criar_dieta_personalizada(self, agent, history=None):
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

    def criar_treino_personalizado(self, agent, history=None):
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

    def escrever_relatorio(self, agent, history=None):
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
            A saída esperada deve ser um texto em formato markdown sem '```', bem formatado e detalhado que descreve:
            - Perfil completo do paciente
            - Dieta personalizada
            - Treino personalizado
            - Recomendações gerais
            """
        )

    def enviar_email(self, agent, history=None):
        history_text = f"\nUtilize o chat history para obter informações:\n{history}" if history else ""
        
        return Task(
            description=f"""
            {history_text}

            Sua tarefa é enviar um email para o paciente com o plano de dieta e o treino personalizado que foi escrito pelo agente redator.
            
            Você deve:
            1. Extrair o email do paciente do histórico da conversa
            2. Criar um título personalizado incluindo o nome do paciente
            3. Usar o relatório final criado pelo agente redator como corpo do email
            4. Enviar o email usando a ferramenta SendEmail com os seguintes parâmetros:
               - subject: O título que você criou
               - message: O relatório completo em formato markdown
               - to_email: O email do paciente extraído do histórico

            IMPORTANTE: Certifique-se de que todos os parâmetros estejam corretos antes de enviar o email.
            """,
            agent=agent,
            expected_output="""
            Um email enviado com sucesso contendo:
            1. Título personalizado com o nome do paciente
            2. Corpo do email com o relatório completo formatado em formato html.
            3. Email do paciente correto
            """
        )

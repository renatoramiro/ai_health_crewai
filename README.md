# AI Health Fitness

Um aplicativo de saúde e fitness que utiliza IA para fornecer orientações personalizadas.

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone [seu-repositorio]
cd ai_health_fitness
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Copie o arquivo `.env.example` para `.env`
- Preencha as variáveis necessárias:
  - `OPENAI_MODEL_NAME`: Nome do modelo OpenAI a ser usado
  - `OPENAI_API_KEY`: Sua chave de API do OpenAI
  - `EVOLUTION_BASE_URL`: URL base da API Evolution
  - `EVOLUTION_API_TOKEN`: Token de API do Evolution
  - `EVOLUTION_INSTANCE`: Instância do Evolution

## Estrutura do Projeto

```
ai_health_fitness/
├── app/
│   └── routes.py         # Rotas da aplicação
├── crew/
│   ├── agents.py         # Definição dos agentes de IA
│   ├── tasks.py          # Tarefas dos agentes
│   └── health_fitness_crew.py  # Lógica principal da crew
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Este arquivo
```

## Desenvolvimento

1. Inicie o servidor de desenvolvimento:
```bash
python app.py
```

2. Acesse a aplicação em `http://localhost:5000`

## Contribuindo

1. Crie um branch para sua feature
2. Faça commit das suas alterações
3. Envie um pull request

## Arquivos Ignorados

O projeto ignora automaticamente:
- Arquivos Python compilados (`*.pyc`, `__pycache__`)
- Ambientes virtuais (`venv/`, `.venv/`)
- Arquivos de IDE (`.vscode/`, `.idea/`)
- Arquivos de ambiente (`.env`)
- Logs e caches

# Base image
FROM python:3.11-slim

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=1

# Instalar dependências do sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários
COPY requirements.txt requirements.txt
COPY app/ app/
COPY crew/ crew/
COPY wsgi.py wsgi.py
COPY gunicorn_config.py gunicorn_config.py

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt && rm -rf ~/.cache/pip

# Expor a porta 5005
EXPOSE 5005

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
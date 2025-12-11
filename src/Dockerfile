# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Metadados da imagem
LABEL maintainer="Carlos Eduardo Favini <favini@microgenesys.com.br>"
LABEL description="Operational Genomics Simulation Environment"
LABEL version="2.0.0"

# Define o diretório de trabalho no container
WORKDIR /app

# Variáveis de ambiente para evitar arquivos .pyc e buffer de stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Adiciona src ao PYTHONPATH para que os imports funcionem corretamente
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Instala as dependências do sistema necessárias (se houver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda a estrutura do projeto
COPY . .

# Cria um usuário não-root por segurança
RUN useradd -m researcher
USER researcher

# Comando padrão: executa a demonstração
CMD ["python", "examples/demo.py"]

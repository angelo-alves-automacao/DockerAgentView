# Dockerfile para Corebot Agent
# Ajuste conforme necessário para o seu projeto

FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /opt/corebot

# Copia requirements (se existir)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Cria diretório para projetos
RUN mkdir -p /opt/corebot/projects

# Define variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV COREBOTPY_DEFAULT=/opt/corebot/projects

# Comando padrão (ajuste conforme necessário)
# Se você tiver um script de entrada, descomente e ajuste:
# COPY agent.py .
# CMD ["python", "agent.py"]

# Por enquanto, mantém o container rodando
CMD ["tail", "-f", "/dev/null"]


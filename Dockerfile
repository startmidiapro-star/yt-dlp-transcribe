# Usa Python
FROM python:3.9-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y ffmpeg

# Copia arquivos
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Porta padrão do Railway
EXPOSE 8080

CMD ["python", "main.py"]

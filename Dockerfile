# Usa uma imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação
COPY . .

# Instala as dependências
RUN pip install -r requirements.txt

# Comando para rodar o programa
CMD ["python", "main.py"]
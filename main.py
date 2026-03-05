import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Agora o os.getenv vai buscar os valores lá dentro
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

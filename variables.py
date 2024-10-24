# variables.py

import os
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurações da API OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4o-mini'  # Ou 'gpt-4-32k' se necessário
TEMPERATURE = 0

# Configurações de Tokens
MAX_TOKENS_DETECTOR = 1  # Para o ReservationDetector (apenas 'Sim' ou 'Não')
MAX_TOKENS_EXTRACTOR = 1500  # Ajuste conforme necessário

# Outros parâmetros
HOTEL_NAME = 'Hotel Vitoria'

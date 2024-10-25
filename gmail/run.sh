#!/bin/bash

# Verificar se o ambiente virtual já existe
if [ ! -d "env" ]; then
  # Criar ambiente virtual
  python -m venv env
fi

# Ativar ambiente virtual
source env/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client flask

# Executar o script Python
python index.py

# Desativar ambiente virtual
deactivate

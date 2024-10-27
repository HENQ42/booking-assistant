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
pip install -r requirements.txt

# Executar o script Python
gunicorn -c gunicorn.conf.py wsgi:app

# Desativar ambiente virtual
deactivate

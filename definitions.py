# definitions.py

import json

# Definição da função para o DataExtractor
DATA_EXTRACTOR_FUNCTION = {
            "type": "function",
            "function": {
                "name": "extrair_dados_reserva",
                "description": "Extrai detalhes de reserva de um e-mail.",
                "parameters": {
                "type": "object",
                "properties": {
                    "nome_cliente": {
                    "type": "string"
                    },
                    "data_check_in": {
                    "type": "string"
                    },
                    "data_check_out": {
                    "type": "string"
                    },
                    "tipo_quarto": {
                    "type": "string"
                    },
                    "numero_hospedes": {
                    "type": "string"
                    },
                    "informacoes_contato": {
                    "type": "string"
                    },
                    "preferencias_especiais": {
                    "type": "string"
                    },
                    "detalhes_pagamento": {
                    "type": "string"
                    }
                },
                "required": [
                    "nome_cliente",
                    "data_check_in",
                    "data_check_out",
                    "tipo_quarto",
                    "numero_hospedes",
                    "informacoes_contato"
                ]
                },
                "strict": False
            }
        }

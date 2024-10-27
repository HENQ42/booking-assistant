# functions.py

from openai import OpenAI
import json
from variables import OPENAI_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS_DETECTOR, MAX_TOKENS_EXTRACTOR, HOTEL_NAME, prompt_system_RESERVARION_DETECTOR, prompt_user_RESERVARION_DETECTOR, prompt_system_DATA_EXTRACTOR
from definitions import DATA_EXTRACTOR_FUNCTION

# Inicialização da API
client = OpenAI()





def reservation_detector(email_content):
    """
    Determina se um e-mail está relacionado a uma reserva no Hotel Vitoria.
    Retorna 'Sim' ou 'Não'.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_system_RESERVARION_DETECTOR},
            {
                "role": "user",
                "content": prompt_user_RESERVARION_DETECTOR(email_content)
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS_DETECTOR,
        n=1,
        stop=None,
    )

    resultado = response.choices[0].message.content.strip()
    return resultado






def data_extractor(email_content):
    """
    Extrai informações específicas de reserva de um e-mail relacionado a uma reserva no Hotel Vitoria.
    Retorna um dicionário com os dados extraídos.
    """
    messages = [
            {
                "role": "system",
                "content": prompt_system_DATA_EXTRACTOR
            },
            {
                "role": "user",
                "content": email_content
            }
        ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS_EXTRACTOR,
        tools=[
            DATA_EXTRACTOR_FUNCTION
        ]
    )

    # Verificar se há chamadas de ferramentas e extrair os argumentos
    if response.choices[0].message.tool_calls:
        function_call = response.choices[0].message.tool_calls[0].function
        arguments = json.loads(function_call.arguments)
        return arguments
    else:
        print("Conteudo Negado!.")
        return "Negado"

    return arguments
# functions.py

from openai import OpenAI
import json
from variables import OPENAI_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS_DETECTOR, MAX_TOKENS_EXTRACTOR, HOTEL_NAME
from definitions import DATA_EXTRACTOR_FUNCTION

# Inicialização da API
client = OpenAI()





def reservation_detector(email_content):
    """
    Determina se um e-mail está relacionado a uma reserva no Hotel Vitoria.
    Retorna 'Sim' ou 'Não'.
    """
    prompt_system = f"""
        Você é o ReservationDetector do {HOTEL_NAME}. Sua tarefa é determinar se um e-mail recebido está relacionado a uma reserva no {HOTEL_NAME}.

                Instruções:

                1. Analise o conteúdo do e-mail fornecido abaixo.

                2. Identifique indicadores de reserva, procurando por palavras-chave e frases como:
                "reserva", "reservar", "quarto", "acomodação", "hospedagem", "check-in", "check-out", "diária", "preço", "disponibilidade".
                Menções diretas ao "{HOTEL_NAME}".

                3. Considere a intenção do remetente:
                O remetente deseja fazer uma reserva ou obter informações sobre hospedagem no {HOTEL_NAME}?
                O e-mail contém perguntas sobre datas, tipos de quarto ou serviços oferecidos?

                4. Responda apenas com:
                "Sim": se o e-mail for relacionado a uma reserva no {HOTEL_NAME}.
                "Não": se o e-mail não estiver relacionado a uma reserva no {HOTEL_NAME}.
    """

    prompt_user = f"""E-mail para análise: {email_content}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_system},
            {
                "role": "user",
                "content": prompt_user
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
                "content": """ 
                        Você é o DataExtractor do Hotel Vitoria. Sua tarefa é extrair informações específicas de reserva de um e-mail relacionado a uma reserva no Hotel Vitoria.
                        Instruções:

                            Analise o conteúdo do e-mail fornecido abaixo.

                            Extraia as seguintes informações:
                                nome_cliente: Se apenas um cliente, então: Nome completo do cliente apenas; se houver mais de um cliente, separe os nomes com ponto e vírgula ';'.
                                data_check_in: Data de entrada (check-in).
                                data_check_out: Data de saída (check-out).
                                tipo_quarto: Tipo de quarto solicitado (ex.: simples, duplo, suíte).
                                numero_hospedes: Quantidade de clientes.
                                informacoes_contato: Informações de contato (e-mail e/ou telefone).
                                preferencias_especiais: Qualquer solicitação ou preferência adicional.
                                detalhes_pagamento: Informações de pagamento, se fornecidas.

                            Considere os detalhes específicos do Hotel Vitoria:
                                Tipos de quartos disponíveis:
                                    Quarto Simples
                                    Quarto Duplo
                                    Suíte Master
                                Facilidades:
                                    Vista para o mar
                                    Café da manhã incluído
                                    Acesso ao spa
                                Políticas:
                                    Check-in a partir das 14h
                                    Check-out até as 12h
                                    Pagamento antecipado ou garantia com cartão de crédito

                            Regras para extração:
                                Datas: Certifique-se de identificar corretamente as datas mencionadas e utilizar o formato DD/MM/AAAA sempre que possível.
                                Nomes: Procure por saudações ou assinaturas para identificar o nome do cliente.
                                Contato: Extraia e-mails, telefones ou outros meios de contato.
                                Preferências: Anote qualquer pedido especial, mesmo que não esteja diretamente relacionado aos serviços listados.
                                Pagamento: Se houver menções como "débito", "cartão de crédito", "Pix", inclua nos detalhes de pagamento.
                                Número de Hóspedes: Se não for explicitamente mencionado, inferir a partir de frases como "eu e minha esposa" (significa 2 pessoas), etc.
                                Dados Ausentes: Se alguma informação não puder ser encontrada, deixe o campo vazio.

                        Resposta:

                            Retorne os dados extraídos chamando a função extrair_dados_reserva com os parâmetros apropriados.
                            Não inclua nenhum texto adicional fora da chamada da função.
                    """
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
        print("Nenhuma função foi chamada.")
        return None

    return arguments
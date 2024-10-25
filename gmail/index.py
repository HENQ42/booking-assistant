import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json
from datetime import datetime, timedelta, timezone
import base64
import requests
from email.mime.text import MIMEText

hours = 10
maxResultsSearch = 2


def load_processed_ids(filename='./data/package.json'):
    # Verificar se o arquivo existe antes de tentar carregá-lo
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f).get('ids', [])
    return []

# Função para salvar os IDs de e-mails processados
def save_processed_ids(processed_ids, filename='./data/package.json'):
    # Criar o diretório ./data/ se ele não existir
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Salvar os IDs no arquivo JSON
    with open(filename, 'w') as f:
        json.dump({'ids': processed_ids}, f)


def get_gmail_service():
    CREDENTIALS_FILE = 'client_secret.json'
    TOKEN_FILE = 'token.json'
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.send'
    ]

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def reply_to_email(message_id, reply_subject, reply_body):
    service = get_gmail_service()

    # Obter a mensagem original
    original_message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    thread_id = original_message['threadId']

    # Extrair o endereço de e-mail do remetente
    headers = original_message['payload']['headers']
    from_email = None
    for header in headers:
        if header['name'] == 'From':
            from_email = header['value']
            break

    # Extrair apenas o e-mail do campo "From"
    if "<" in from_email and ">" in from_email:
        from_email = from_email.split("<")[1].split(">")[0]  # Extrai apenas o e-mail entre "<" e ">"

    if not from_email:
        print("Não foi possível encontrar o endereço de e-mail do remetente.")
        return

    # Criar a mensagem de resposta
    message = MIMEText(reply_body)
    message['to'] = from_email
    message['subject'] = reply_subject
    message['In-Reply-To'] = original_message['id']
    message['References'] = original_message['id']

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message_body = {
        'raw': raw_message,
        'threadId': thread_id
    }

    # Enviar a mensagem
    sent_message = service.users().messages().send(userId='me', body=message_body).execute()
    print(f"Mensagem enviada com sucesso. ID: {sent_message['id']}")

    # Marcar a mensagem original como lida
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print("Mensagem original marcada como lida.")


def print_last_emails(service):
    hour_ago = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp())
    
    # Carregar IDs dos e-mails já processados
    processed_ids = load_processed_ids()

    # Adicionar o filtro "is:unread" e "after:" com o timestamp
    query = f"is:unread after:{hour_ago} category:primary"
    response = service.users().messages().list(userId='me', q=query, maxResults=maxResultsSearch).execute()
    messages = response.get('messages', [])

    if not messages:
        print(f"Nenhum e-mail não lido encontrado nas últimas {hours} hora(s).")
        return

    new_processed_ids = []

    for i, message in enumerate(messages):
        if message['id'] in processed_ids:
            continue  # Pular e-mails já processados

        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        snippet = msg.get('snippet', '')
        headers = msg['payload']['headers']
        
        subject = None
        from_email = None
        content = snippet  # Aqui atribuímos o 'snippet' ao 'content'

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                from_email = header['value']


        # Obter o conteúdo completo do e-mail (text/plain)
        if "parts" in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':  # Conteúdo em texto simples
                    data = part['body']['data']
                    content = base64.urlsafe_b64decode(data).decode('utf-8')
                    break



        print('\nfazendo request')
        # Fazer requisição HTTP para processar o conteúdo do e-mail
        response = requests.post('http://localhost:5000/process-email', json={"email_content": content})
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            response_data = response.json()
            
            # Verificar se a resposta contém "status": "success" e "is_reservation": true
            if response_data.get('status') == 'success' and response_data.get('is_reservation') is True:
                # Lógica adicional quando o status é "success" e is_reservation é true
                print(f"Reserva detectada no e-mail {i+1}: {subject}\n")
                
                # Enviando Confirmação.
                print("Respondendo e-mail\n")
                reply_to_email(message['id'], 'Re: Análise e Resposta Automática', "Reserva Confirmada!")

            else:
                print(f"E-mail {i+1} processado, mas sem reserva detectada.\n")
        else:
            print(f"Erro ao processar o e-mail {i+1}: {response.status_code}")


        
        print(f"E-mail {i+1}:")
        print(f"Assunto: {subject}")
        print(f"De: {from_email}")
        print(f"Resumo: {snippet}\n")
        # print(f"Conteúdo completo do e-mail:\n{content}\n")

        # Adicionar o ID deste e-mail à lista de processados
        new_processed_ids.append(message['id'])

    # Atualizar e salvar os IDs processados
    processed_ids.extend(new_processed_ids)
    save_processed_ids(processed_ids)


def main():
    print("Iniciando a verificação de e-mails...")
    service = get_gmail_service()
    print_last_emails(service)

if __name__ == '__main__':
    main()
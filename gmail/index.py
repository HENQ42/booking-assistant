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

hours = 10
maxResultsSearch = 1


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


def print_last_emails(service):
    hour_ago = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp())
    
    # Carregar IDs dos e-mails já processados
    processed_ids = load_processed_ids()

    # Adicionar o filtro "is:unread" e "after:" com o timestamp
    query = f"is:unread after:{hour_ago} category:primary -is:reply"
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
            if header['name'] == 'Date':
                sent_date = header['value']


        # Obter o conteúdo completo do e-mail (text/plain)
        if "parts" in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':  # Conteúdo em texto simples
                    data = part['body']['data']
                    content = base64.urlsafe_b64decode(data).decode('utf-8')
                    break



        print('\nfazendo request')
        # Fazer requisição HTTP para processar o conteúdo do e-mail
        response = requests.post('http://localhost:5003/process-email', json={"email_content": "Data do email: "+sent_date+"\n"+content})
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            response_data = response.json()
            
            # Verificar se a resposta contém "status": "success" e "is_reservation": true
            if response_data.get('status') == 'success' and response_data.get('is_reservation') is True:
                # Lógica adicional quando o status é "success" e is_reservation é true
                print("dados: ", response_data)
                print(f"Reserva detectada no e-mail {i+1}: {subject}\n")


                # Preparar os dados para a fila de confirmação
                confirmation_data = {
                    "message_id": message['id'],
                    "subject": subject,
                    "from_email": from_email,
                    "sent_date": sent_date,
                    "reservation_details": response_data
                }


                # Enviar dados para a fila de confirmação
                print("dados a serem enviados: ", confirmation_data)
                confirm_response = requests.post('http://localhost:5001/api/queue_email', json=confirmation_data, headers={'Content-Type': 'application/json'})
                if confirm_response.status_code == 201:
                    print("Dados enviados para a fila de confirmação com sucesso.")
                else:
                    print(f"Erro ao enviar para a fila de confirmação: {confirm_response.status_code}")



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
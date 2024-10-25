# reply_email.py

from index import get_gmail_service
import base64
from email.mime.text import MIMEText

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




if __name__ == "__main__":
    # ID da mensagem que você deseja responder
    message_id = 'INSIRA_O_ID_DA_MENSAGEM_AQUI'

    # Dados da nova mensagem (dados fictícios indicando que é um teste)
    reply_subject = 'Re: Teste de Resposta Automática'
    reply_body = '''Olá,



Esta é uma resposta automática de teste. Por favor, desconsidere este e-mail.

Atenciosamente,
Sua Equipe'''

# Chamar a função para responder ao e-mail
reply_to_email('INSIRA_O_ID_DA_MENSAGEM_AQUI', 'Re: Teste de Resposta Automática', "Reserva Confirmada!")

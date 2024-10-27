from flask import Flask, request, jsonify
from index import get_gmail_service
import base64
from email.mime.text import MIMEText

app = Flask(__name__)


# Definindo o assunto e o corpo padrão
reply_subject = "Reserva Confirmada!"
reply_body = "Sua reserva foi confirmada com sucesso."



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
        from_email = from_email.split("<")[1].split(">")[0]

    if not from_email:
        return {"error": "Não foi possível encontrar o endereço de e-mail do remetente."}, 400

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
    
    # Marcar a mensagem original como lida
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

    return {"success": True, "message_id": sent_message['id']}

@app.route('/reply_email', methods=['POST'])
def reply_email_route():
    data = request.json
    message_id = data.get("message_id")

    # Verifica se o 'message_id' foi fornecido
    if not message_id:
        return jsonify({"error": "O campo 'message_id' é obrigatório."}), 400

    # Chamada da função reply_to_email com os dados padrões
    response = reply_to_email(message_id, reply_subject, reply_body)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5004)
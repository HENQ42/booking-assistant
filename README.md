# booking-assistant
  run-assistant: gunicorn -c gunicorn.conf.py wsgi:app
  run-gmail-pipe: sh /gmail/run.sh

# Request
  url: http://localhost:5000/process-email
  body: { "email_content": "{content}" }

# Config Gmail Pipe
  1. Criar credencial no console.cloud.google.com
  2. Criar ID do cliente do OAuth (App para computador)
  3. baixar, inserir e renomear no diretorio /gmail/client_secret.json
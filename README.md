# booking-assistant
  run: gunicorn -c gunicorn.conf.py wsgi:app

# Request
  url: http://localhost:5000/process-email
  body: { "email_content": "{content}" }

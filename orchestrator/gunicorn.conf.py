from variables import PORT_GPT

bind = "0.0.0.0:"+PORT_GPT
workers = 1
timeout = 15
#gunicorn -c gunicorn.conf.py wsgi:app
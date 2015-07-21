FROM python:2.7

RUN pip install pip==6.1.1

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

ENV PORT=80

EXPOSE 80

CMD gunicorn -b 0.0.0.0:$PORT --log-file=- --error-logfile=- --access-logfile=- -k eventlet -w 2 natalieandjoe.wsgi:application

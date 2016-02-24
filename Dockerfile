FROM python:3.5-alpine


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN  pip3 install --no-cache-dir --upgrade --ignore-installed flask hvac

COPY app.py /usr/src/app
COPY certs.pem  /usr/src/app/certs.pem

CMD ["python", "app.py"]

FROM python:3.8.1-alpine3.11

COPY run.py /bin/gitea-cgit-adapter
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD ["gitea-cgit-adapter"]

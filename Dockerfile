FROM python:3.8.1-alpine3.11

COPY run.py /app/gitea-cgit-adapter
COPY cgit-template.txt /app/cgit-template.txt
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD ["/app/gitea-cgit-adapter"]

FROM python:3.9-alpine

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY cgit-template.txt /app/cgit-template.txt

COPY run.py /app/gitea-cgit-adapter

CMD ["/app/gitea-cgit-adapter"]

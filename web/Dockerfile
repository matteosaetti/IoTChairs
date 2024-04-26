FROM python:3.8-slim

WORKDIR /

COPY common/ /web/app

WORKDIR /web/app

COPY /web/app/requirementsWebApp.txt .

RUN pip install -r requirementsWebApp.txt

COPY /web/app .

CMD ["python", "app.py"]
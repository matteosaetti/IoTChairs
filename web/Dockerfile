FROM python:3.8-slim

WORKDIR /

WORKDIR /web/app

COPY /web/requirementsWebApp.txt .

RUN pip install -r requirementsWebApp.txt

COPY /web .

CMD ["python", "app.py"]
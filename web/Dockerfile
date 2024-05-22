FROM python:3.12-slim

WORKDIR /

WORKDIR /web/app

COPY /web/requirementsWebApp.txt .

RUN pip install -r requirementsWebApp.txt

COPY /web .

CMD ["python", "app.py"]

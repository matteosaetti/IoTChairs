FROM python:3.12-slim

WORKDIR /web/app

COPY /web/app/requirementsWebApp.txt .

RUN pip install -r requirementsWebApp.txt

COPY /web/app .

CMD ["python", "app.py"]

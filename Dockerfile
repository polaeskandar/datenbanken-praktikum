FROM python:3.14.0a2-slim-bullseye

RUN apt update && apt install sqlite3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]

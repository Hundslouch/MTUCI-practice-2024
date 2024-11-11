FROM python:3.12-bullseye

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD alembic upgrade head && python3 /app/bot/main.py
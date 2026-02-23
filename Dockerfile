FROM python:3.13-alpine
WORKDIR /app
COPY board.py engine.py game.py main.py ./
CMD ["python", "-u", "main.py"]

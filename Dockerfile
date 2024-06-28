FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir poetry && \
    poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-ansi

CMD gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8080
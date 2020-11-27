FROM python:3.7

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    DATA_LOCATION=./data

COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && \
    poetry install --no-dev

COPY . .

EXPOSE 80

CMD ["poetry", "run", "python", "-m", "scholar_data_digest.api"]

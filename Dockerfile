FROM python:3.7

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    DATA_LOCATION=./data

COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && \
    poetry install --no-dev

COPY . .

RUN cd /app/data && \
    mkdir /data && \
    cd /app/src/ldig/models && \
    tar -xzf model.latin.tar.gz && \
    mv model.latin /data/model.latin

EXPOSE 80

CMD ["poetry", "run", "python", "-m", "scholar_data_ingest.api"]

import logging
import os
from random import randrange
from typing import Any, Dict, List, Set

import psycopg2


_LOGGER = logging.getLogger(__package__)
# _LOGGER.info(f"------> {os.environ}")

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

HOST = "host.docker.internal"  # quickfix

conn = psycopg2.connect(
    f"port=5432 host={HOST} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"
)
cur = conn.cursor()


def test() -> None:
    pass

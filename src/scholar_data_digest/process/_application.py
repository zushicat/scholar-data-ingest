import logging
from typing import Any, Dict, List, Tuple

# from ._postgres_adapter import test
from ._ingester import ingest_bulk

_LOGGER = logging.getLogger(__package__)


# *****
# Is it alive? (Kind of a debug method.)
# *****
def ping() -> Dict[str, str]:
    return {"status": "ok", "response": "pong"}


# ****
#
# ****
def ingest_bulk_dispatch(files: str) -> Dict[str, str]:
    ingest_bulk(files)
    return {"status": "ok", "response": "ingested"}

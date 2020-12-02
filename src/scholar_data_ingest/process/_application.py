import logging
from typing import Any, Dict, List, Tuple

# from ._postgres_adapter import test
from ._ingester import export_table_csv, ingest_bulk, truncate_table

_LOGGER = logging.getLogger(__package__)


# *****
# Is it alive? (Kind of a debug method.)
# *****
def ping() -> Dict[str, str]:
    return {"status": "ok", "response": "pong"}


# ****
#
# ****
def ingest_bulk_dispatch(files: str, use_lang_detection: bool) -> Dict[str, str]:
    ingest_bulk(files, use_lang_detection)
    return {"status": "ok", "response": "ingested"}


# ****
#
# ****
def truncate_table_dispatch(table_names: str) -> Dict[str, str]:
    truncate_table(table_names)
    return {"status": "ok", "response": "truncated"}


# ****
#
# ****
def export_csv_dispatch(table_names: str) -> Dict[str, str]:
    export_table_csv(table_names)
    return {"status": "ok", "response": "csv exported"}
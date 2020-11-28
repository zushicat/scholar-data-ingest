import csv
import datetime
import json
import os
import logging
from typing import Any, Dict, List, Optional, Tuple

# from ._postgres_adapter import test

_LOGGER = logging.getLogger(__package__)

DIRNAME = os.environ["DATA_LOCATION"]


def _get_file_json_line(filename: str) -> Optional[List[Dict[str, Any]]]:
    #try:
    data: List[Dict[str, Any]] = []
    with open(f"{DIRNAME}/tmp/{filename}") as f:
        filedata: List[str] = f.read().split("\n")
    for line_str in filedata:
        line_data: Dict[str, Any] = json.loads(line_str)
        data.append(line_data)
        break
    return data
    # except Exception as e:
    #     return None


def ingest_bulk(filenames: str) -> None:
    for filename in filenames:
        data = _get_file_json_line(filename)
        _LOGGER.info(data)
        break

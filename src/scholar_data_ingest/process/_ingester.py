import csv
import datetime
import json
import os
import logging
from typing import Any, Dict, List, Optional, Tuple

# from ._postgres_adapter import test

_LOGGER = logging.getLogger(__package__)

DIRNAME = os.environ["DATA_LOCATION"]


# *******
# write into DB (with _postgres_adapter methods)
# *******
def _write_table_text(data: Dict[str, Any]) -> None:
    pass
    

def _write_table_author(data: Dict[str, Any]) -> None:
    pass


def _write_table_paper(data: Dict[str, Any]) -> None:
    pass


def _set_db_entry(incoming: Dict[str, Any]) -> bool:
    try:
        _LOGGER.info("---------> hello")
        return True
    except Exception as e:
        return False


def _process_bulk_file(filename: str) -> Tuple[Optional[int], Optional[int]]:
    '''
    Process lines of single bulk JSON line file (approx. 30000 lines).
    Write each parsed line directly into DB (with method: _set_db_entry).
    '''
    try:
        count_written_ok: int = 0
        with open(f"{DIRNAME}/tmp/{filename}") as f:
            lines: List[str] = f.read().split("\n")
        for line in lines:
            try:
                line_data: Dict[str, Any] = json.loads(line)
                if _set_db_entry(line_data) is True:
                    count_written_ok += 1
            except Exception as e:
                # _LOGGER.info(f"ERROR 1 ---> {e}")
                continue
            break
        return count_written_ok, len(lines)
    except Exception as e:
        # _LOGGER.info(f"ERROR 0 ---> {e}")
        return None, None


def ingest_bulk(filenames: str) -> None:
    for filename in filenames:
        count_processed, count_all = _process_bulk_file(filename)
        _LOGGER.info(f"{count_processed}, {count_all}")
        break

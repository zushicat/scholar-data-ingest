import json
import os
import logging
from typing import Any, Dict, List, Optional, Tuple
import uuid

from ._postgres_adapter import write_initial_DB
from ldig import ldig


_LOGGER = logging.getLogger(__package__)
DIRNAME = os.environ["DATA_LOCATION"]

ldig.check_loaded_model()


# *******
# write into DB tables (with _postgres_adapter methods)
# *******
def _write_table_text(data: Dict[str, Any]) -> None:
    is_written: bool = write_initial_DB("text", data, "paper_id")
    

def _write_table_author(data: Dict[str, Any]) -> None:
    is_written: bool = write_initial_DB("author", data, "author_ids")
    # _LOGGER.info(f"----> {is_written}")


def _write_table_paper(data: Dict[str, Any]) -> None:
    is_written: bool = write_initial_DB("paper", data, "paper_id")


# *******
# initiate DB entries of line
# *******
def _set_db_entry(data: Dict[str, Any]) -> bool:
    try:
        # ***
        # check if entry is valid: MUST have a title and min. 1 author
        # ***
        if data["title"] is None or len(data["title"]) < 10:  
            return False
        if data["authors"] is None or len(data["authors"]) == 0:
            return False

        text_id: str = str(uuid.uuid4())

        # ***
        # check for language
        # ***
        check_title: str = data["title"]  # "私は猫で幸せです。"
        check_abstract: str = data["paperAbstract"] if data["paperAbstract"] is not None else ""
        detected_language, confidence = ldig.detect(f"{check_title} {check_abstract}")
        
        if confidence < 0.5:  # needs to be confident enough
            detected_language = None
        
        # set empty abstract entry to None
        data["paperAbstract"] = None if data["paperAbstract"] is None or len(data["paperAbstract"]) == 0 else data["paperAbstract"]

        # ***
        # process table text entry
        # ***
        _write_table_text({
            "text_id": text_id,
            "paper_id": data["id"],
            "title": data["title"],
            "abstract": data["paperAbstract"],
            "language": detected_language
        })

        # ***
        # process table author entries
        # ***
        all_author_ids = []  # collect ids
        for author in data["authors"]:
            all_author_ids += author["ids"]
            _write_table_author({
                "author_ids": ",".join(author["ids"]),
                "name": author["name"]
            })

        # ***
        # process table paper entry
        # ***
        _write_table_paper({
            "paper_id": data["id"],
            "year_published": data["year"],
            "author_ids": ",".join(all_author_ids),
            "research_fields": ",".join(data["fieldsOfStudy"]),
            "text_id": text_id,
            "is_cited_ids": ",".join(data["inCitations"]) if len(data["inCitations"]) > 0 else None,
            "has_cited_ids": ",".join(data["outCitations"]) if len(data["outCitations"]) > 0 else None
        })
        
        return True
    except Exception as e:
        _LOGGER.info(f"ERROR ---> {e}")
        return False


# *******
# process all incoming bulk data per line
# *******
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
        return count_written_ok, len(lines)
    except Exception as e:
        # _LOGGER.info(f"ERROR 0 ---> {e}")
        return None, None


def ingest_bulk(filenames: str) -> None:
    for filename in filenames:
        count_processed, count_all = _process_bulk_file(filename)
        _LOGGER.info(f"{count_processed}, {count_all}")

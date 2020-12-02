import json
import os
import logging
from typing import Any, Dict, List, Optional, Tuple
import uuid

from ._postgres_adapter import db_bulk_insert_into_table, db_truncate_table
from ldig import ldig  # language detection


_LOGGER = logging.getLogger(__package__)
DIRNAME = os.environ["DATA_LOCATION"]
USE_LANG_DETECTION = False

ldig.check_loaded_model()  # load latin model for language detection


# *******
# create data according to DB schema per line
# *******
def _create_table_entries(data: Dict[str, Any], use_lang_detection: bool=False) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
    try:
        # ***
        # check if entry is valid: MUST have a title and min. 1 author
        # ***
        if data["title"] is None or len(data["title"]) < 10:  
            return False
        if data["authors"] is None or len(data["authors"]) == 0:
            return False

        text_id: str = str(uuid.uuid4())

        detected_language: Optional[str] = None

        # ***
        # check for language
        # ***
        if use_lang_detection is True:
            try:
                shortened_title: str = " ".join(data["title"].split(" ")[:4])  # use the first n words
            except Exception:
                shortened_title: str = data["title"]
            detected_language, confidence = ldig.detect(shortened_title)
            
            if confidence < 0.5:  # needs to be confident enough
                detected_language = None
        

        # set empty abstract entry to None
        data["paperAbstract"] = None if data["paperAbstract"] is None or len(data["paperAbstract"]) == 0 else data["paperAbstract"]

        # ***
        # 
        # ***
        table_text_entry = {
            "text_id": text_id,
            "paper_id": data["id"],
            "title": data["title"],
            "abstract": data["paperAbstract"],
            "language": detected_language
        }

        # ***
        # 
        # ***
        all_author_ids = []  # collect ids, keep order of authors
        table_author_entries: List[Dict[str, Any]] = []

        for author in data["authors"]:
            '''
            author["ids"] is List[str], therefore make redundant entries if number of ids > 1
            Also, only use the first author id in paper reference.
            (The case of redundant entries may never happen, but is theoretically possible.)
            '''
            for i, current_id in enumerate(author["ids"]):
                if i == 0:
                    all_author_ids.append(current_id)

                also_referring_ids = ",".join([x for x in author["ids"] if x != current_id])
                if len(also_referring_ids) == 0:
                    also_referring_ids = None
                
                table_author_entries.append({
                    "author_id": current_id,
                    "name": author["name"],
                    "also_referring_ids": also_referring_ids
                })

        # ***
        # 
        # ***
        table_paper_entry = {
            "paper_id": data["id"],
            "year_published": data["year"],
            "author_ids": ",".join(all_author_ids),
            "research_fields": ",".join(data["fieldsOfStudy"]),
            "text_id": text_id,
            "is_cited_ids": ",".join(data["inCitations"]) if len(data["inCitations"]) > 0 else None,
            "has_cited_ids": ",".join(data["outCitations"]) if len(data["outCitations"]) > 0 else None
        }
        
        return table_paper_entry, table_text_entry, table_author_entries
    except Exception as e:
        _LOGGER.info(f"ERROR ---> {e}")
        return None, None, None

# *******
# process all incoming bulk data per line (dict -> DB schema)
# write bulk in DB
# *******
def _process_bulk_file(filename: str) -> None:
    table_paper_data: List[Dict[str, Any]] = []
    table_text_data: List[Dict[str, Any]] = []
    table_author_data: List[Dict[str, Any]] = []
    try:
        with open(f"{DIRNAME}/tmp/{filename}") as f:
            lines: List[str] = f.read().split("\n")
        for i, line in enumerate(lines):
            if i%1000 == 0:
                _LOGGER.info(f"-- {filename} {i} --")

            try:
                line_data: Dict[str, Any] = json.loads(line)
                table_paper_entry, table_text_entry, table_author_entries = _create_table_entries(data=line_data, use_lang_detection=USE_LANG_DETECTION)
            
                table_paper_data.append(table_paper_entry)
                table_text_data.append(table_text_entry)
                table_author_data += table_author_entries
            
            except Exception as e:
                # _LOGGER.info(f"ERROR 1 ---> {e}")
                continue
    except Exception as e:
        # _LOGGER.info(f"ERROR 0 ---> {e}")
        pass
    
    # _LOGGER.info(f"---> {table_paper_data}")
    # _LOGGER.info(f"---> {table_author_data}")
    # _LOGGER.info(f"---> {table_text_data}")

    db_bulk_insert_into_table("paper", table_paper_data)
    db_bulk_insert_into_table("text", table_text_data)
    db_bulk_insert_into_table("author", table_author_data)


def ingest_bulk(filenames: str, use_lang_detection: bool) -> None:
    '''
    TODO: use COPY for bulk import into DB instead of INSERT (in DB adapter)
    '''
    global USE_LANG_DETECTION

    USE_LANG_DETECTION = use_lang_detection
    for filename in filenames:
        _LOGGER.info(f"Process ---> {filename}")
        _process_bulk_file(filename)
        
        _LOGGER.info(f"Done.")

def truncate_table(table_names: List[str]) -> None:
    for table_name in table_names:
        db_truncate_table(table_name)

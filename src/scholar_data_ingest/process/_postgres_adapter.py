import logging
import os
from random import randrange
from typing import Any, Dict, List, Set

import psycopg2
from psycopg2.extensions import AsIs  # https://stackoverflow.com/a/29471241


_LOGGER = logging.getLogger(__package__)
# _LOGGER.info(f"------> {os.environ}")

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

HOST = "host.docker.internal"  # quickfix

CONNECTION = psycopg2.connect(
    f"port=5432 host={HOST} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"
)


def write_initial_DB(table_name: str, data: Dict[str, Any], reference_id_name: str) -> bool:
    '''
    Generic insert statement from dict: https://stackoverflow.com/a/29471241
    Check if reference_id is already in table. (Can be single or comma separated string.)
    If existing: write entry (return True)
    else: as of now just SKIP

    TODO: make more efficient with copying data batch (https://www.dataquest.io/blog/loading-data-into-postgres/)
    '''
    cursor = CONNECTION.cursor()

    # reference ids (here) are always strings
    reference_id_value = data[reference_id_name]
    sql_query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {reference_id_name} = '{reference_id_value}');"
    cursor.execute(sql_query)
    is_existing: bool = cursor.fetchone()

    # _LOGGER.info(f"{reference_id_value} {is_existing}")

    columns = data.keys()
    values = [data[column] for column in columns]
    if True in is_existing:
        # skip (usually some update mechanism would be useful)
        return False
    
    # ***
    # write new entry
    # ***
    try:
        sql_query = f"INSERT INTO {table_name} (%s) VALUES %s;"

        # _LOGGER.info(cursor.mogrify(sql_query, (AsIs(','.join(columns)), tuple(values))))
        cursor.execute(sql_query, (AsIs(",".join(columns)), tuple(values)))
        CONNECTION.commit()

        return True
    except Exception as e:
        _LOGGER.info(f"SQL ERROR -----> {e}")

        cursor.execute("ROLLBACK")
        CONNECTION.commit()
        return False


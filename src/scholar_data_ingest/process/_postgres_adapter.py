import logging
import os
from random import randrange
from typing import Any, Dict, List, Set

import psycopg2
# from psycopg2.extensions import AsIs  # https://stackoverflow.com/a/29471241
from psycopg2.extras import execute_values  # https://stackoverflow.com/a/54949835


_LOGGER = logging.getLogger(__package__)
# _LOGGER.info(f"------> {os.environ}")

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

HOST = "host.docker.internal"  # quickfix

CONNECTION = psycopg2.connect(
    f"port=5432 host={HOST} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"
)


def db_insert_into_table(table_name: str, data: Dict[str, Any], reference_id_name: str) -> bool:
    '''
    ! NOT USED !
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


def db_bulk_insert_into_table(table_name: str, data: List[Dict[str, Any]]) -> bool:
    '''
    Write entries in bulk.
    See: https://stackoverflow.com/a/54949835
    As for now: simply ignore in case of (id) confict (instead of update).
    '''
    cursor = CONNECTION.cursor()

    id_reference: str = f"{table_name}_id"
    
    columns = ",".join(list(data[0].keys()))
    sql_query = f"INSERT INTO {table_name} ({columns}) VALUES %s ON CONFLICT ({id_reference}) DO NOTHING;"
    values = [[v for v in d.values()] for d in data]

    execute_values(cursor, sql_query, values)
    CONNECTION.commit()


def db_truncate_table(table_name: str) -> bool:
    try:
        cursor = CONNECTION.cursor()
        sql_query = f"TRUNCATE TABLE {table_name}; ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"
        cursor.execute(sql_query)
        CONNECTION.commit()

        return True
    except Exception as e:
        return False

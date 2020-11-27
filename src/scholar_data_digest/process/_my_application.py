import csv
import datetime
import json
import os
import logging
from typing import Any, Dict, List, Tuple

from ._postgres_adapter import test


_LOGGER = logging.getLogger(__package__)

DIRNAME = os.environ["DATA_LOCATION"]

# *****
# Is it alive? (Kind of a debug method.)
# *****
def ping() -> Dict[str, str]:
    return {"status": "ok", "response": "pong"}

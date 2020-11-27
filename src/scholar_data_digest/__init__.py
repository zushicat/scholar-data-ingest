import logging
import logging.config
import os

working_dir = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(os.path.join(working_dir, "logging_config.ini"))
logging.getLogger().setLevel(os.environ.get("LOG_LEVEL", "INFO"))  # "DEBUG"

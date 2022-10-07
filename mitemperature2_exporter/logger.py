# -*- coding: utf-8 -*-

import logging
from app_config import app_config

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET

logging.basicConfig(
    filename=app_config()["app"]["logfile"],
    encoding="utf-8",
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger()


def get_logger():
    return logger

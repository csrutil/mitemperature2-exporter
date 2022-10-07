# -*- coding: utf-8 -*-

import logging

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET

logging.basicConfig(
    filename="mitemperature2-exporter.log",
    encoding="utf-8",
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger()


def get_logger():
    return logger

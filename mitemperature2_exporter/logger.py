# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger()

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_logger():
    return logger


# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET

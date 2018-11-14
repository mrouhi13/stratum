'''Simple wrapper around python's logging package'''
from __future__ import absolute_import

import os
import logging
from twisted.python import log as twisted_log

from . import settings

def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.setLevel(getattr(logging, settings.LOGLEVEL))

    if settings.LOGFILE != None:
        logger.addHandler(file_handler)

    logger.debug("Logging initialized")
    return logger

if settings.DEBUG:
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(module)s.%(funcName)s # %(message)s")
else:
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s # %(message)s")

if settings.LOGFILE != None:
    file_handler = logging.FileHandler(os.path.join(settings.LOGDIR, settings.LOGFILE))
    file_handler.setFormatter(fmt)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(fmt)

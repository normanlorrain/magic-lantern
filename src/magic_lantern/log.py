# A friendly wrapper for Python's logging

import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from importlib.metadata import version

# Import these for use by client code.
# "noqa" is for Flake8; warning is ignored
from logging import error, debug, warning, info, exception  # noqa: F401


def init():

    DEBUG_LOG = Path("magic-lantern-debug.log")
    ERROR_LOG = Path("magic-lantern-error.log")

    # Start with a fresh log
    DEBUG_LOG.unlink(missing_ok=True)
    ERROR_LOG.unlink(missing_ok=True)

    MAX_BYTES = 100000
    BACKUP_COUNT = 1

    # Not sure if this is what we want.  TBD
    # if platform.system() == "Windows":
    #     filename = Path(os.getcwd()) / filename
    # else:
    #     filename = Path("/var/log") / filename

    # set up logging to file - see previous section for more details
    LONGFORMAT = (
        "%(asctime)s\t"
        "%(levelname)s\t"
        "%(filename)14s:%(lineno)s\t"
        "%(funcName)-14s\t"
        "%(message)s"
        # "\t%(name)s"
    )
    # SHORTFORMAT = "%(filename)s:%(lineno)s\t%(message)s"
    SHORTFORMAT = "%(message)s"

    # Root logger gets everything.  Handlers defined below will filter it out...
    logging.getLogger("").setLevel(logging.DEBUG)

    # The exifread package is very chatty for this application.
    # Not everything has EXIF data.
    logging.getLogger("exifread").setLevel(logging.ERROR)

    debugHandler = RotatingFileHandler(
        Path(DEBUG_LOG), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    debugHandler.setLevel(logging.DEBUG)
    debugHandler.setFormatter(logging.Formatter(LONGFORMAT))
    logging.getLogger("").addHandler(debugHandler)

    errorHandler = RotatingFileHandler(
        Path(ERROR_LOG),
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    errorHandler.setLevel(logging.ERROR)
    errorHandler.setFormatter(logging.Formatter(LONGFORMAT))
    logging.getLogger("").addHandler(errorHandler)

    # define a Handler which writes to sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(SHORTFORMAT))
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)

    logging.info("Application started.")
    logging.info(f"Version: {version(__package__)}")
    logging.info(f"Args: {' '.join(sys.argv)}")
    logging.info(f"Logging to {DEBUG_LOG} and {ERROR_LOG}")

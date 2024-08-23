from logging import *
from logging.handlers import RotatingFileHandler
from pathlib import Path


DEBUG_LOG = "magic-lantern-debug.log"
ERROR_LOG = "magic-lantern-error.log"

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
    "%(message)s\t"
    # "%(name)s\t"
)
SHORTFORMAT = "%(filename)s:%(lineno)s\t%(message)s"

# Root logger gets everything.  Handlers defined below will filter it out...
getLogger("").setLevel(DEBUG)

# The exifread package is very chatty for this application.  Not everything has EXIF data.
getLogger("exifread").setLevel(ERROR)

# define a Handler which writes to sys.stderr
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(Formatter(SHORTFORMAT))
# add the handler to the root logger
getLogger("").addHandler(console)


debugHandler = RotatingFileHandler(
    Path(DEBUG_LOG), mode="w", maxBytes=100000, backupCount=1, encoding="utf-8"
)
debugHandler.setLevel(DEBUG)
debugHandler.setFormatter(Formatter(LONGFORMAT))
getLogger("").addHandler(debugHandler)

errorHandler = RotatingFileHandler(
    Path(ERROR_LOG),
    mode="w",
    maxBytes=100000,
    backupCount=1,
    encoding="utf-8",
)
errorHandler.setLevel(ERROR)
errorHandler.setFormatter(Formatter(LONGFORMAT))
getLogger("").addHandler(errorHandler)

info(f"Logging to {DEBUG_LOG} and {ERROR_LOG}")

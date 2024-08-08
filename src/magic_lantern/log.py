from logging import *
from pathlib import Path

# set up logging to file - see previous section for more details
LONGFORMAT = (
    "%(filename)s:%(lineno)s : "
    "%(message)25s :: "
    "%(name)s:%(levelname)s:"
    "%(asctime)s: "
)
SHORTFORMAT = "%(filename)s:%(lineno)s - %(message)s"

# Root logger gets everything.  Handlers defined below will filter it out...

getLogger("").setLevel(DEBUG)

getLogger("exifread").setLevel(ERROR)


def init(filename=Path("magic_lantern.log")):
    filehandler = FileHandler(filename, mode="w", encoding="utf-8")
    filehandler.setLevel(DEBUG)
    filehandler.setFormatter(Formatter(LONGFORMAT))
    getLogger("").addHandler(filehandler)
    info(f"Logging to {filename.absolute()}")


# define a Handler which writes to sys.stderr
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(Formatter(SHORTFORMAT))
# add the handler to the root logger
getLogger("").addHandler(console)

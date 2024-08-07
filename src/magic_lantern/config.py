import pathlib
import os
import enum
import tomllib
import sys

this_mod = sys.modules[__name__]

configRoot: pathlib.Path = None
fullscreen: bool = False
interval: int = 5

EXCLUDE = "exclude"
ALBUMS = "albums"
ORDER = "order"
FOLDER = "folder"
WEIGHT = "weight"
INTERVAL = "interval"


class Order(enum.StrEnum):
    SEQUENCE = "sequence"
    ATOMIC = "atomic"
    RANDOM = "random"


def init(
    configFile: pathlib.Path | None,
    fullscreen_: bool,
    shuffle: bool,
    interval_: int,
    path: pathlib.Path,
):
    # Save the command line option here
    global fullscreen
    fullscreen = fullscreen_

    # This is the folder that the slides are found in
    global configRoot
    if configFile:
        configRoot = configFile.parent
        _dictConfig = loadConfig(configFile)
    else:  # create a simple album
        configRoot = os.getcwd()
        _dictConfig = createConfig(path, shuffle)

    for i in _dictConfig:
        setattr(this_mod, i, _dictConfig[i])
    pass

    # If the config file doesn't specify a weight, set it here.
    # Each album can set it's own weight which will override this.
    if not hasattr(this_mod, WEIGHT):
        setattr(this_mod, WEIGHT, 1)

    # If the config file doesn't specify an interval, set it here.
    # Each album can set it's own interval which will override this.
    if not hasattr(this_mod, INTERVAL):
        setattr(this_mod, INTERVAL, 1)

    # This is passed from the command line, and thus overrides any setting that
    # came from the config file above.
    global interval
    interval = interval_


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createConfig(path, shuffle):

    return {
        ALBUMS: [{ORDER: "random" if shuffle else "sequence", FOLDER: path, WEIGHT: 1}]
    }

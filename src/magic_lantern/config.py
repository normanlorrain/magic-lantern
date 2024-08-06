import pathlib
import os
import enum
import tomllib

_dictConfig = None
configRoot: pathlib.Path = None
fullscreen: bool = False
interval: int = 5

ALBUMS = "albums"
ORDER = "order"
FOLDER = "folder"
WEIGHT = "weight"


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
    global _dictConfig
    global configRoot
    global fullscreen
    global interval

    fullscreen = fullscreen_
    interval = interval_

    if configFile:
        configRoot = configFile.parent
        _dictConfig = loadConfig(configFile)
    else:  # create a simple album
        configRoot = os.getcwd()
        _dictConfig = createConfig(path, shuffle)


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createConfig(path, shuffle):

    return {
        ALBUMS: [{ORDER: "random" if shuffle else "sequence", FOLDER: path, WEIGHT: 1}]
    }

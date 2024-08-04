import pathlib
import os
import enum
import tomllib

_configRoot: pathlib.Path = None
_fullscreen: bool = False

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
    fullscreen: bool,
    shuffle: bool,
    path: pathlib.Path,
):
    global _dictConfig
    global _fullscreen
    global _configRoot

    if configFile:
        _configRoot = configFile.parent
        _dictConfig = loadConfig(configFile)
    else:  # create a simple album
        _configRoot = os.getcwd()
        _dictConfig = createConfig(path, shuffle)
    _fullscreen = fullscreen


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createConfig(path, shuffle):

    return {
        ALBUMS: [{ORDER: "random" if shuffle else "sequence", FOLDER: path, WEIGHT: 1}]
    }

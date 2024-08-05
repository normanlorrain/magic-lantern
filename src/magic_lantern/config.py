import pathlib
import os
import enum
import tomllib

configRoot: pathlib.Path = None
fullscreen: bool = False

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
    full_screen: bool,
    shuffle: bool,
    path: pathlib.Path,
):
    global _dictConfig
    global fullscreen
    global configRoot

    if configFile:
        configRoot = configFile.parent
        _dictConfig = loadConfig(configFile)
    else:  # create a simple album
        configRoot = os.getcwd()
        _dictConfig = createConfig(path, shuffle)
    fullscreen = full_screen


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createConfig(path, shuffle):

    return {
        ALBUMS: [{ORDER: "random" if shuffle else "sequence", FOLDER: path, WEIGHT: 1}]
    }

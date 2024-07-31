import os
import pathlib

import tomllib
from slideshow.album import Album, Order

_configRoot: pathlib.Path = None
_fullscreen: bool = False

ALBUMS = "albums"
ORDER = "order"
FOLDER = "folder"
WEIGHT = "weight"


def init(configFile: pathlib.Path, fullscreen: bool, shuffle: bool, path: pathlib.Path):
    global _dictConfig
    global _fullscreen
    global _configRoot

    if configFile:
        _configRoot = configFile.parent
        _dictConfig = loadConfig(configFile)
    else:  # create a simple album
        _dictConfig = createConfig(path, shuffle)
    _fullscreen = fullscreen


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createConfig(path, shuffle):
    album = Album(path, shuffle)
    return [album]

import os
import pathlib

import tomllib
from slideshow.album import Album, Order

_configRoot: pathlib.Path = None

CONFIG_ALBUMS = "albums"
CONFIG_ORDER = "order"
CONFIG_FOLDER = "folder"
CONFIG_WEIGHT = "weight"


def init(configFile):
    global _dictConfig
    global _albumList
    _dictConfig = loadConfig(configFile)
    _albumList = createAlbums(_dictConfig)


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createAlbums(dictConfig: dict):
    albumList = []
    for dictAlbum in dictConfig[CONFIG_ALBUMS]:

        order = dictAlbum[CONFIG_ORDER]
        if order not in Order:
            raise Exception(f"Bad Config: {order} not in {[e.value for e in Order]}")

        path = _configRoot / dictAlbum[CONFIG_FOLDER]
        if not path.exists():
            raise Exception(f"bad Config: invalid path: {path}")

        weight = dictAlbum.get(CONFIG_WEIGHT, 0)
        if not isinstance(weight, int):
            raise Exception(f"Bad Config: weight {weight} should be integer")

        album = Album(order, path, weight)
        albumList.append(album)
    return albumList


def createConfig(path, shuffle):
    album = Album(path, shuffle)
    return [album]

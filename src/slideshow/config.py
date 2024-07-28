import tomllib
from slideshow.album import Album, Order


def init(configFile):
    global _cfg
    global _albumList
    _cfg = loadConfig(configFile)
    _albumList = createAlbums(_cfg)


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createAlbums(dictConfig: dict):
    albumList = []
    for dictAlbum in dictConfig["albums"]:
        order = dictAlbum["order"]
        path = dictAlbum["folder"]
        weight = dictAlbum.get("weight", 0)

        album = Album(order, path, weight)
        albumList.append(album)
    return albumList


def createConfig(path, shuffle):
    album = Album(path, shuffle)
    return [album]

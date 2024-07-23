import tomllib
from slideshow.album import Album


def load_config(config):
    with open(config, "rb") as fp:
        global toml
        toml = tomllib.load(fp)
    global _albumList
    _albumList = []
    for albums in toml["albums"]:
        pass


def create_config(path, shuffle):
    album = Album(path, shuffle)
    return [album]

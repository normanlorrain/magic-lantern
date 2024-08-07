import random

from magic_lantern.photo import Photo
from magic_lantern.album import Album
from magic_lantern.config import Order
from magic_lantern import config


_photoList: list[Photo] = []
_photoIndex: int = -1
_photoCount: int = 0


def init():
    albumList: list[Album] = []
    albumWeights: list[int] = []
    totalPhotos = 0

    for dictAlbum in config.albums:

        order = dictAlbum[config.ORDER]
        if order not in [e.value for e in Order]:
            raise Exception(f"Bad Config: {order} not in {[e.value for e in Order]}")

        path = config.configRoot / dictAlbum[config.FOLDER]
        if not path.exists():
            raise Exception(f"bad Config: invalid path: {path}")

        weight = dictAlbum.get(config.WEIGHT, 1)
        if not isinstance(weight, int):
            raise Exception(f"Bad Config: weight {weight} should be integer")

        album = Album(order, path, weight)
        albumList.append(album)
        albumWeights.append(weight)
        totalPhotos += album._photoCount

    # Build a list of photos from random albums
    global _photoList
    global _photoCount
    previousAlbum = None
    for album in random.choices(albumList, albumWeights, k=totalPhotos * 100):
        if album._order == Order.ATOMIC:
            if previousAlbum == album:
                print("preventing atomic album from repeating")
                continue
            while photo := album.getNextPhoto():
                _photoList.append(photo)
                # print(photo.filename)
        else:
            photo = album.getNextPhoto()
            _photoList.append(photo)
            # print(photo.filename)
        previousAlbum = album
    _photoCount = len(_photoList)


def getNextPhoto():
    global _photoList
    global _photoIndex
    global _photoCount
    _photoIndex += 1
    if _photoIndex >= _photoCount:
        _photoIndex = 0
    return _photoList[_photoIndex]


def getPreviousPhoto():
    global _photoList
    global _photoIndex
    global _photoCount
    _photoIndex -= 1
    if _photoIndex < 0:
        _photoIndex = 0
    return _photoList[_photoIndex]


def getCurrentPhoto():
    global _photoList
    global _photoIndex
    global _photoCount
    return _photoList[_photoIndex]

import pytest

from slideshow import config

TEST_CFG = {
    "albums": [
        {"order": "sequence", "folder": "tests/photos/numbers", "weight": 10},
        {"order": "atomic", "folder": "test/photos/atomic", "weight": 20},
        {"order": "random", "folder": "test/photos/paintings", "weight": 20},
        {"order": "sequence", "folder": "test/pdfs"},
    ]
}


def testLoadConfig(pytestconfig):
    cfg = config.loadConfig(pytestconfig.rootpath / "tests/example.toml")
    pass


def testCreateAlbums():
    albums = config.createAlbums(TEST_CFG)
    pass


# def testInit(pytestconfig):
#     config.init(pytestconfig.rootpath / "tests/configs/slideshow.toml")
#     pass

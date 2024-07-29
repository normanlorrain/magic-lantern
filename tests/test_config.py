import pytest

from slideshow import config

TEST_CFG = {
    "albums": [
        {"order": "sequence", "folder": "photos/numbers", "weight": 10},
        {"order": "atomic", "folder": "photos/atomic", "weight": 20},
        {"order": "random", "folder": "photos/paintings", "weight": 20},
        {"order": "sequence", "folder": "pdfs"},
    ]
}


def testLoadConfig(pytestconfig):
    cfg = config.loadConfig(pytestconfig.rootpath / "tests/example.toml")
    pass


def testCreateAlbums(pytestconfig):
    config._configRoot = pytestconfig.rootpath / "tests"
    albums = config.createAlbums(TEST_CFG)
    pass


# def testInit(pytestconfig):
#     config.init(pytestconfig.rootpath / "tests/configs/slideshow.toml")
#     pass

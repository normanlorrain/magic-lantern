import pytest

from slideshow import config

TEST_CFG = {
    "albums": [
        {"order": "sequence", "folder": "images/numbers", "weight": 10},
        {"order": "atomic", "folder": "images/atomic", "weight": 20},
        {"order": "random", "folder": "images/paintings", "weight": 20},
        {"order": "sequence", "folder": "pdfs"},
    ]
}


def testLoadConfig(pytestconfig):
    cfg = config.loadConfig(pytestconfig.rootpath / "tests/example.toml")
    pass


def testCreateConfig(pytestconfig):
    cfg = config.createConfig("/a/b/c", True)
    pass


# def testInit(pytestconfig):
#     config.init(pytestconfig.rootpath / "tests/configs/slideshow.toml")
#     pass

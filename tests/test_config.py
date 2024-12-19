# import pytest
import pathlib
from types import SimpleNamespace

from magic_lantern import config


TEST_CFG = {
    "albums": [
        {"order": "sequence", "folder": "images/numbers", "weight": 10},
        {"order": "atomic", "folder": "images/atomic", "weight": 20},
        {"order": "random", "folder": "images/paintings", "weight": 20},
        {"order": "sequence", "folder": "pdfs"},
    ]
}


def mockLoadConfig(cfg_file):
    print(cfg_file)
    return {
        config.EXCLUDE: (),
        config.FULLSCREEN: False,
        config.SHUFFLE: False,
        config.INTERVAL: 5,
        config.ALBUMS: [
            {
                config.FOLDER: "/foo/bar/wha",
                config.ORDER: config.Order.RANDOM,
            }
        ],
    }


def testLoadConfig(pytestconfig):
    config.loadConfig = mockLoadConfig

    commandLineContext = SimpleNamespace(
        params={
            config.CONFIG_FILE: pathlib.Path("/home/foo/foo.toml"),
            "directory": None,
        }
    )
    # ctx.params = {}
    config.init(commandLineContext)

    pass

import pathlib
import os
import enum
import tomllib
import sys
from types import SimpleNamespace
from magic_lantern import log

# Global configuration attributes:
#    - config_file
#    - fullscreen
#    - shuffle
#    - interval
#    - path


this_mod = sys.modules[__name__]

albums: list = []

EXCLUDE = "exclude"
FULLSCREEN = "fullscreen"
ALBUMS = "albums"
ORDER = "order"
FOLDER = "folder"
WEIGHT = "weight"
INTERVAL = "interval"


class Order(enum.StrEnum):
    SEQUENCE = "sequence"
    ATOMIC = "atomic"
    RANDOM = "random"


defaults = {
    EXCLUDE: [],
    FULLSCREEN: False,
    ORDER: Order.SEQUENCE,
    WEIGHT: 1,
    INTERVAL: 5,
}


def init(ctx):
    # We're working with a full config file
    # if hasattr(this_mod, "config_file"):
    if "config_file" in ctx.params:
        setattr(this_mod, "config_file", ctx.params["config_file"])
        setattr(this_mod, "config_parent", this_mod.config_file.parent)
        dictConfig = loadConfig(this_mod.config_file)


 #TODO

    # We're working with a simple directory
    elif hasattr(this_mod, "directory"):
        Set the "global" parameters, if the command line has them
        for param, value in ctx.params.items():
            if value is None:
                continue
            setattr(this_mod, param, value)
        pass

        dictConfig = {ALBUMS: [{FOLDER: this_mod.directory}]}


#TODO


    else:
        raise Exception("No config or directory given.")

    # Set the global parameters from the configuration
    # (command line has priority, done above)
    for i in dictConfig:
        if i == ALBUMS:
            continue  # We handle the albums later
        if not hasattr(this_mod, i):
            setattr(this_mod, i, dictConfig[i])
    pass

    # Set any remaining missing values from the defaults
    for i in defaults:
        if not hasattr(this_mod, i):
            setattr(this_mod, i, defaults[i])

    # Validate the albums. Make a copy first, then loop
    # and update with validated fields
    # albumList = list()
    for album in dictConfig[ALBUMS]:
        try:
            validateAlbumPath(album)
            validateAlbumOrder(album)
            validateAlbumWeight(album)
            validateAlbumInterval(album)
            albums.append(SimpleNamespace(**album))
        except ValidationError as e:
            log.error(e)

    # # If the config file doesn't specify a weight, set it here.
    # # Each album can set it's own weight which will override this.
    # if not hasattr(this_mod, WEIGHT):
    #     setattr(this_mod, WEIGHT, 1)

    # # If the config file doesn't specify exclude, set it here.
    # if not hasattr(this_mod, EXCLUDE):
    #     setattr(this_mod, EXCLUDE, [])

    # # If the config file doesn't specify an interval, set it here.
    # # Each album can set it's own interval which will override this.
    # if not hasattr(this_mod, INTERVAL):
    #     setattr(this_mod, INTERVAL, 1)

    # # This is passed from the command line, and thus overrides any setting that
    # # came from the config file above.
    # if interval_:
    #     global interval
    #     interval = interval_

    # # This is passed from the command line, and thus overrides any setting that
    # # came from the config file above.
    # if fullscreen_:
    #     global fullscreen
    #     fullscreen = fullscreen_


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


class ValidationError(Exception):
    pass


def validateAlbumWeight(album):
    if WEIGHT in album:
        if not isinstance(album[WEIGHT], int):
            raise ValidationError("Configuration: bad value for {key} in album {path}")
    else:
        album[WEIGHT] = this_mod.weight


def validateAlbumInterval(album):
    if INTERVAL in album:
        if not isinstance(album[INTERVAL], int):
            raise ValidationError("Configuration: bad value for {key} in album {path}")
    else:
        album[INTERVAL] = this_mod.interval


def validateAlbumOrder(album):
    if ORDER in album:
        if album[ORDER] not in [e.value for e in Order]:
            raise ValidationError(
                "Configuration: bad value for {ORDER} in album {path}"
            )


def validateAlbumPath(album: dict):
    path = pathlib.Path(album[FOLDER])

    # If the configured path is relative,
    # prepend the path of the config file
    if not path.is_absolute():
        if hasattr(this_mod, "config_file"):
            path = this_mod.config_file.parent / path

    if path.exists():
        album[FOLDER] = path
    else:
        raise ValidationError(f"Configuration: invalid path: {path}")

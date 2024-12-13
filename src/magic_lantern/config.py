import pathlib
import enum
import tomllib
import sys
from types import SimpleNamespace
from magic_lantern import log


# General configuration attributes:
#    - config_file
#    - directory
#    - fullscreen
#    - shuffle
#    - interval
#    - path
# Album-specific configuration attributes:
#    - order
#    - folder
#    - weight
#    - interval


this_mod = sys.modules[__name__]

albums: list = []

# Configuration file string constants
# These are also used as command-line Click options
# See cli.py
CONFIG_FILE = "config_file"
DIRECTORY = "directory"
EXCLUDE = "exclude"
FULLSCREEN = "fullscreen"
SHUFFLE = "shuffle"
ALBUMS = "albums"
ORDER = "order"
FOLDER = "folder"
WEIGHT = "weight"
INTERVAL = "interval"


class Order(enum.StrEnum):
    SEQUENCE = "sequence"
    ATOMIC = "atomic"
    RANDOM = "random"


# General defaults
defaults = {
    EXCLUDE: [],
    FULLSCREEN: False,
    SHUFFLE: False,
    INTERVAL: 5,
}

# Album-specific defaults
album_defaults = {
    ORDER: Order.SEQUENCE,
    WEIGHT: 1,
}


class ConfigurationError(Exception):
    pass


def init(ctx):
    # Configuration starts with what was on the command line
    # Convert the parameters to attributes of this module
    for param, value in ctx.params.items():
        setattr(this_mod, param, value)

    # If we're working with a full config file...
    if this_mod.config_file:
        with open(this_mod.config_file, "rb") as fp:
            try:
                dictConfig = tomllib.load(fp)
            except tomllib.TOMLDecodeError as e:
                log.error(f"Configuration file error: {this_mod.config_file}")
                raise ConfigurationError(e)

    # If we're working with a simple directory, create a bare-bones configuration
    # to start with.

    elif this_mod.directory:
        # Note: this directory name is guaranteed to be absolute per Click
        dictConfig = {ALBUMS: [{FOLDER: this_mod.directory}]}

    else:
        raise ConfigurationError("No config or directory given.")

    # Set the global parameters from the configuration
    for i in dictConfig:
        if i == ALBUMS:
            # We handle the albums later, because some "global"
            # options may be relevant
            continue
        if i not in defaults:
            raise ConfigurationError(f"Bad config file entry: {i}")
        if hasattr(this_mod, i):
            value = getattr(this_mod, i)
            if isinstance(value, bool):
                setattr(this_mod, i, value or dictConfig[i])
        else:
            setattr(this_mod, i, dictConfig[i])

    # Set any remaining missing values from the defaults
    for i in defaults:
        if not hasattr(this_mod, i) or getattr(this_mod, i) is None:
            setattr(this_mod, i, defaults[i])

    # Validate the albums.
    for album in dictConfig[ALBUMS]:
        try:
            validateAlbumFolder(album)
            validateAlbumOrder(album)
            validateAlbumWeight(album)
            validateAlbumInterval(album)
            albums.append(SimpleNamespace(**album))
        except ConfigurationError as e:
            log.error(e)


def validateAlbumWeight(album):
    if WEIGHT in album:
        if not isinstance(album[WEIGHT], int):
            raise ConfigurationError(
                "Configuration: bad value for {key} in album {path}"
            )
    else:
        album[WEIGHT] = album_defaults[WEIGHT]


def validateAlbumInterval(album):
    if INTERVAL in album:
        if not isinstance(album[INTERVAL], int):
            raise ConfigurationError(
                "Configuration: bad value for {key} in album {path}"
            )
    else:
        album[INTERVAL] = this_mod.interval


def validateAlbumOrder(album):
    if ORDER in album:
        if album[ORDER] not in [e.value for e in Order]:
            raise ConfigurationError(
                "Configuration: bad value for {ORDER} in album {path}"
            )
    else:
        album[ORDER] = album_defaults[ORDER]


def validateAlbumFolder(album: dict):
    if this_mod.directory:  # Validation done by click
        return

    # If we reach this point the folder is an entry in the
    # config file.  Make it absolute and verify it exists
    path = pathlib.Path(album[FOLDER])
    if not path.is_absolute():
        path = this_mod.config_file.parent / path

    if path.exists():
        album[FOLDER] = path
    else:
        raise ConfigurationError(f"Configuration error. Invalid path: {path}")

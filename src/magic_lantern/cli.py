import sys
import click
import pathlib

from magic_lantern import log, config, controller

log.init()
log.info(f"Application started.")
log.info(f"Args: {' '.join(sys.argv)}")


@click.command(
    epilog="See https://github.com/normanlorrain/magic-lantern for more details."
)
@click.version_option()
@click.option(
    "-c",
    "--config-file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    help="Configuration file.",
)
@click.option(
    "-f", "--fullscreen", is_flag=True, show_default=True, help="Full screen mode"
)
@click.option(
    "-s", "--shuffle", is_flag=True, show_default=True, help="Shuffle the slides"
)
@click.option(
    "-i",
    "--interval",
    type=click.IntRange(min=1, max=None),
    required=False,
    help="Interval (seconds) between images.",
)
@click.argument(
    "directory",
    type=click.Path(
        exists=True, resolve_path=True, dir_okay=True, path_type=pathlib.Path
    ),
    required=False,
)
def magic_lantern(config_file, fullscreen, shuffle, interval, directory):
    """A slide show generator. Specify a directory containing image files or use -c to specify a config file."""
    if config_file == None and directory == None:
        raise click.ClickException("Must specify a DIRECTORY or a config file.")
    if config_file and directory:
        log.warn(
            "Warning: -c and DIRECTORY are mutually exclusive. DIRECTORY will be ignored"
        )
    if directory:
        log.info(f"Single directory slide show: {directory}")

    config.init(config_file, fullscreen, shuffle, interval, directory)
    controller.init()
    controller.run()


def cli():
    try:
        magic_lantern()
    except SystemExit:
        log.info("Application ended normally (System Exit)")
    except KeyboardInterrupt:
        log.warn("Application ended (KeyboardInterrupt)")
    except Exception as e:
        log.exception("Application ended. (UNCAUGHT EXCEPTION)")

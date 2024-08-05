import click
import pathlib
import os

# suppresses Pygame message on import
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from magic_lantern import config, slideshow, screen, text, controller


@click.command(
    epilog="See https://github.com/normanlorrain/magic-lantern for more details"
)
@click.option(
    "-c",
    "--config-file",
    "file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    help="Configuration file.",
)
@click.option("-f", "--fullscreen", is_flag=True, help="Full screen mode")
@click.option("-s", "--shuffle", is_flag=True, help="shuffle the photos")
@click.argument(
    "directory",
    type=click.Path(
        exists=True, resolve_path=True, dir_okay=True, path_type=pathlib.Path
    ),
    required=False,
)
def magic_lantern(file, fullscreen, shuffle, directory):
    """A slide show generator. Specify a directory containing image files or use -c to specify a config file."""
    if directory:
        click.echo(f"magic_lantern: {directory}")
        if file:
            click.echo(
                "Warning: -c and DIRECTORY are mutually exclusive. DIRECTORY will be ignored"
            )
    if file == None and directory == None:
        raise click.ClickException("Must specify a DIRECTORY or a config file.")

    config.init(file, fullscreen, shuffle, directory)
    screen.init()  # Needs to be before the rest, so Pygame gets initalized.
    slideshow.init()
    text.init()
    controller.init()
    controller.run()


def cli():
    magic_lantern()

import click
import pathlib

from magic_lantern import config, slideshow, screen, text, controller


@click.command()
@click.option(
    "-c",
    "--config-file",
    type=click.Path(
        exists=True, resolve_path=True, file_okay=True, path_type=pathlib.Path
    ),
    help="Configuration file.  PATH is ignored.",
)
@click.option("-f", "--fullscreen", is_flag=True, help="Full screen mode")
@click.option("-s", "--shuffle", is_flag=True, help="shuffle the photos")
@click.argument(
    "path",
    type=click.Path(
        exists=True, resolve_path=True, dir_okay=True, path_type=pathlib.Path
    ),
    required=False,
)
def magic_lantern(config_file, fullscreen, shuffle, path):
    """magic_lantern generator. Specify a PATH or use -c to specify a config file."""
    if path:
        click.echo(f"magic_lantern: {path}")
        if config_file:
            click.echo(
                "Warning: -c and PATH are mutually exclusive. PATH will be ignored"
            )
    if config_file == None and path == None:
        raise click.ClickException("Must specify a PATH or a config file.")

    config.init(config_file, fullscreen, shuffle, path)
    screen.init()  # Needs to be before the rest, so Pygame gets initalized.
    slideshow.init()
    text.init()
    controller.init()
    controller.run()


def cli():
    magic_lantern()

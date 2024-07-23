import click

from slideshow import controller
from slideshow import config


@click.command()
@click.option("-c", "--config-file", help="Configuration file.  PATH is ignored.")
@click.option("-f", "--fullscreen", is_flag=True, help="Full screen mode")
@click.option("-s", "--shuffle", is_flag=True, help="shuffle the photos")
@click.argument("path", type=click.Path(exists=True), required=False)
def slideshow(config_file, fullscreen, shuffle, path):
    """Slideshow generator. Specify a PATH or use -c to specify a config file."""
    if path:
        click.echo(f"Slideshow: {path}")
        if config_file:
            click.echo(
                "Warning: -c and PATH are mutually exclusive. PATH will be ignored"
            )
    if config_file:
        configuration = config.load_config(config_file)
    else:
        configuration = config.create_config(path)

    if config_file == None and path == None:
        raise click.ClickException("Must specify a PATH or a config file.")

    config.fullscreen = fullscreen
    config.shuffle = shuffle

    controller.init(config)
    controller.run()


def cli():
    slideshow()

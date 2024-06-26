import click

from slideshow import controller


@click.command()
@click.option("-f", "--fullscreen", is_flag=True)
@click.argument("path", required=True)
def slideshow(fullscreen, path):
    """Slideshow generator."""
    click.echo(path)
    controller.init(path, fullscreen)
    controller.run()


def cli():
    slideshow()

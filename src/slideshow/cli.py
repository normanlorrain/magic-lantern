import click

from slideshow import controller


@click.command()
@click.argument("path", required=True)
def slideshow(path):
    """Slideshow generator."""
    click.echo(path)
    controller.init(path)
    controller.run()


def cli():
    slideshow()

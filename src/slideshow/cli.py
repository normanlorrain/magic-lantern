import click

from slideshow import controller


@click.command()
@click.option("-f", "--fullscreen", is_flag=True, help="Full screen mode")
@click.option("-s", "--shuffle", is_flag=True, help="shuffle the photos")
@click.argument("path", required=True)
def slideshow(fullscreen, shuffle, path):
    """Slideshow generator."""
    click.echo(f"Slideshow: {path}")
    controller.init(path, fullscreen, shuffle)
    controller.run()


def cli():
    slideshow()

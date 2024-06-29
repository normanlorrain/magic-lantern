import os
from slideshow import cli

if "SLIDESHOW_PROFILE" in os.environ:
    import cProfile

    cProfile.run("cli()", sort="time")
else:
    cli()

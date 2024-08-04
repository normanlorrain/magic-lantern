import os
from magic_lantern import cli

if "magic_lantern_PROFILE" in os.environ:
    import cProfile

    cProfile.run("cli()", sort="time")
else:
    cli()

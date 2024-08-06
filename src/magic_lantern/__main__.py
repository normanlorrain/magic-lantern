import os
from magic_lantern import cli

# To invoke the profiler, set this environment variable and run as a module
# i.e. python -m magic_lantern ....
if "MAGIC_LANTERN_PROFILE" in os.environ:
    import cProfile

    cProfile.run("cli()", sort="time")
else:
    cli()

from slideshow import cli
import cProfile

cProfile.run("cli()", sort="time")

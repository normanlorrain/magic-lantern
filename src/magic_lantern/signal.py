# An interface the the OS signal API, so we can accept SIGURS1 signals.

import signal
import os

import pygame
from magic_lantern import log

SIGUSR1_EVENT = pygame.event.custom_type()


def handler(signum, _):
    log.info(f"Signal handler called with signal {signum}")
    pygame.event.post(pygame.event.Event(SIGUSR1_EVENT))


def init():
    if os.name == "posix":
        signal.signal(signal.SIGUSR1, handler)
        log.info(f"Signal handler initialised. We are pid: {os.getpid()}")
        log.info("To reset slideshow run:")
        log.info("pkill -USR1 magic-lantern")

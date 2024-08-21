from pathlib import Path

import pygame

from magic_lantern import log, config
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

WATCHDOG_EVENT = pygame.event.custom_type()

_observer = None


def init():
    _observer = Observer()
    for dictAlbum in config.albums:
        path = Path(dictAlbum[config.FOLDER])
        event_handler = EventHandler()
        _observer.schedule(event_handler, path, recursive=True)
        log.info(f"monitoring: {path}")
    _observer.start()


def quit():
    _observer.stop()
    _observer.join()


class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        log.debug(f"Filesystem changes detected: {event}")
        log.info(f"File was {event.event_type}")
        pygame.event.post(pygame.event.Event(WATCHDOG_EVENT))

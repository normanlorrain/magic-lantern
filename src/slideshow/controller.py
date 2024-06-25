import time
import pygame

from slideshow import album
from slideshow import screen

photoList = []

PHOTO_EVENT = pygame.event.custom_type()
PHOTO_INTERVAL = 3000
LOOP_INTERVAL = 100  # msec


def init(path):
    screen.init()
    album.init(path)


def showNewPhoto():
    # Blank the screen
    screen.displaySurface.fill((0, 0, 0))
    # for photo in photoList:
    photo = album.getNextPhoto()
    screen.displaySurface.blit(photo.getSurface(), photo.transform())

    # flip() the display to put your work on screen
    pygame.display.flip()


def run():
    # Creates a periodically repeating event on the event queue
    pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)

    showNewPhoto()
    while True:
        event = pygame.event.wait(LOOP_INTERVAL)
        if event.type == PHOTO_EVENT:
            showNewPhoto()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                break
            if event.key in [pygame.K_n, pygame.K_RIGHT]:
                showNewPhoto()
        pygame.event.clear()
    pygame.quit()

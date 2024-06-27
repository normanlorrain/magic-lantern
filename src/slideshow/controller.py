from enum import auto

import pygame

from slideshow import album
from slideshow import screen
from slideshow import text

photoList = []

PHOTO_EVENT = pygame.event.custom_type()
PHOTO_INTERVAL = 3000
LOOP_INTERVAL = 100  # msec

pauseState = False
infoState = False

NEXT = auto()
PREVIOUS = auto()


def init(path, fullscreen):

    screen.init(fullscreen)
    text.init()
    album.init(path)


def showNewPhoto(direction=NEXT):
    # Blank the screen
    screen.displaySurface.fill((0, 0, 0))

    if direction == NEXT:
        photo = album.getNextPhoto()
    if direction == PREVIOUS:
        photo = album.getPreviousPhoto()

    screen.displaySurface.blit(photo.getSurface(), photo.coordinates())

    if infoState:
        datetime = text.createMessage(str(photo.datetime))
        screen.displaySurface.blit(datetime, (0, screen.HEIGHT - datetime.get_height()))

    # flip() the display to put your work on screen
    pygame.display.flip()
    return photo


def pause(photo):
    if pauseState:
        pygame.time.set_timer(PHOTO_EVENT, 0)

        screen.displaySurface.blit(text.createMessage("PAUSE"), (0, 0))

        filename = text.createMessage(str(photo.filename))
        x = screen.WIDTH - filename.get_width()
        y = screen.HEIGHT - filename.get_height()
        screen.displaySurface.blit(filename, (x, y))

        datetime = text.createMessage(str(photo.datetime))
        x = 0
        y = screen.HEIGHT - datetime.get_height()
        screen.displaySurface.blit(datetime, (0, y))

        pygame.display.flip()
    else:
        showNewPhoto()
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def run():
    global pauseState
    global infoState
    # Creates a periodically repeating event on the event queue
    pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)

    photo = showNewPhoto()
    while True:
        event = pygame.event.wait(LOOP_INTERVAL)
        if event.type == pygame.NOEVENT:
            continue
        print(event)
        if event.type == PHOTO_EVENT:
            if not pauseState:
                photo = showNewPhoto()
        if event.type in [pygame.WINDOWCLOSE, pygame.QUIT]:
            break
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                break
            if event.key in [pygame.K_n, pygame.K_RIGHT]:
                photo = showNewPhoto()
            if event.key in [pygame.K_p, pygame.K_LEFT]:
                photo = showNewPhoto(PREVIOUS)
            if event.key == pygame.K_i:
                infoState = not infoState
            if event.key == pygame.K_SPACE:
                pauseState = not pauseState
                pause(photo)
        # pygame.event.clear()
    pygame.quit()

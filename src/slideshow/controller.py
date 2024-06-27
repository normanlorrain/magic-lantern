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
showYearState = True

NEXT = auto()
PREVIOUS = auto()


def init(path, fullscreen, shuffle):

    screen.init(fullscreen)
    text.init()
    album.init(path, shuffle)


def showNewPhoto(direction=NEXT):
    # Blank the screen
    screen.displaySurface.fill((0, 0, 0))

    if direction == NEXT:
        photo = album.getNextPhoto()
    if direction == PREVIOUS:
        photo = album.getPreviousPhoto()

    screen.displaySurface.blit(photo.getSurface(), photo.coordinates())

    showMetaData()

    # flip() the display to put your work on screen
    pygame.display.flip()


# if infoState:
#     datetime = text.createMessage(str(photo.datetime))
#     screen.displaySurface.blit(datetime, (0, screen.HEIGHT - datetime.get_height()))

pad = 10


def showMetaData():
    photo = album.getCurrentPhoto()
    if pauseState:

        screen.displaySurface.blit(text.createMessage("PAUSE"), (pad, pad))

        filename = text.createMessage(str(photo.filename))
        x = screen.WIDTH - filename.get_width() - pad
        y = screen.HEIGHT - filename.get_height() - pad
        screen.displaySurface.blit(filename, (x, y))

        datetime = text.createMessage(str(photo.datetime))
        x = 0 + pad
        y = screen.HEIGHT - datetime.get_height() - pad
        screen.displaySurface.blit(datetime, (x, y))

    if showYearState:
        year = text.createMessage(str(photo.datetime)[0:4], text.HEADING, (163, 48, 42))
        x = screen.WIDTH - year.get_width() - pad
        y = 0 + pad
        screen.displaySurface.blit(year, (x, y))
    pygame.display.flip()


def pause():
    global pauseState
    pauseState = not pauseState
    if pauseState:
        pygame.time.set_timer(PHOTO_EVENT, 0)
        showMetaData()

    else:
        showNewPhoto()
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def year():
    global showYearState
    showYearState = not showYearState
    if not showYearState:  # Remove the year by redrawing
        screen.displaySurface.fill((0, 0, 0))
        photo = album.getCurrentPhoto()
        screen.displaySurface.blit(photo.getSurface(), photo.coordinates())
    showMetaData()


def next():
    showNewPhoto()
    if not pauseState:
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def previous():
    showNewPhoto(PREVIOUS)
    if not pauseState:
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def run():
    global pauseState
    global showYearState
    # Creates a periodically repeating event on the event queue
    pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)

    showNewPhoto()
    while True:
        event = pygame.event.wait(LOOP_INTERVAL)
        if event.type == pygame.NOEVENT:
            continue
        print(event)
        if event.type == PHOTO_EVENT:
            if not pauseState:
                showNewPhoto()
        if event.type in [pygame.WINDOWCLOSE, pygame.QUIT]:
            break
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                break
            if event.key in [pygame.K_n, pygame.K_RIGHT]:
                next()
            if event.key in [pygame.K_p, pygame.K_LEFT]:
                previous()
            if event.key == pygame.K_y:
                year()
            if event.key == pygame.K_SPACE:
                pause()

        # pygame.event.clear()
    pygame.quit()

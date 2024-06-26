import time
import pygame

from slideshow import album
from slideshow import screen
from slideshow import text

photoList = []

PHOTO_EVENT = pygame.event.custom_type()
PHOTO_INTERVAL = 3000
LOOP_INTERVAL = 100  # msec

pauseState = False


def init(path, fullscreen):

    screen.init(fullscreen)
    text.init()
    album.init(path)


def showNewPhoto():
    # Blank the screen
    screen.displaySurface.fill((0, 0, 0))
    # for photo in photoList:
    photo = album.getNextPhoto()
    screen.displaySurface.blit(photo.getSurface(), photo.coordinates())

    datetime = text.createMessage(str(photo.datetime))
    screen.displaySurface.blit(datetime, (0, screen.HEIGHT - datetime.get_height()))

    # flip() the display to put your work on screen
    pygame.display.flip()


def pause():
    if pauseState:
        pygame.time.set_timer(PHOTO_EVENT, 0)

        screen.displaySurface.blit(text.createMessage("PAUSE"), (0, 0))
        pygame.display.flip()
    else:
        showNewPhoto()
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def run():
    global pauseState
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
                showNewPhoto()
            if event.key == pygame.K_SPACE:
                pauseState = not pauseState
                pause()
        # pygame.event.clear()
    pygame.quit()

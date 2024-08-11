from enum import auto

import pygame

from magic_lantern import slideshow
from magic_lantern import screen
from magic_lantern import text
from magic_lantern import config
from magic_lantern import log
from magic_lantern.slide import SlideException

PHOTO_EVENT = pygame.event.custom_type()
PHOTO_INTERVAL = None
LOOP_INTERVAL = 1000  # msec

pauseState = False
showYearState = False

NEXT = auto()
PREVIOUS = auto()


def init():
    global PHOTO_INTERVAL
    PHOTO_INTERVAL = config.interval * 1000  # msec
    pygame.key.set_repeat(500, 100)


def showNewSlide(direction=NEXT):
    # Blank the screen
    screen.displaySurface.fill((0, 0, 0))

    while True:
        try:
            if direction == NEXT:
                slide = slideshow.getNextSlide()
            if direction == PREVIOUS:
                slide = slideshow.getPreviousSlide()
            break
        except SlideException as e:
            log.warn(f"Bad slide file: {e.filename}")

    log.debug(f"{slide.filename} interval:{slide.interval}")
    screen.displaySurface.blit(slide.getSurface(), slide.coordinates())

    showMetaData()

    # flip() the display to put your work on screen
    pygame.display.flip()
    global PHOTO_INTERVAL
    PHOTO_INTERVAL = slide.interval * 1000  # msec


def showMetaData():
    pad = 10
    slide = slideshow.getCurrentSlide()
    if pauseState:

        screen.displaySurface.blit(text.createMessage("PAUSE"), (pad, pad))

        filename = text.createMessage(str(slide.filename))
        x = screen.WIDTH - filename.get_width() - pad
        y = screen.HEIGHT - filename.get_height() - pad
        screen.displaySurface.blit(filename, (x, y))

        datetime = text.createMessage(str(slide.datetime))
        x = 0 + pad
        y = screen.HEIGHT - datetime.get_height() - pad
        screen.displaySurface.blit(datetime, (x, y))

    if showYearState:
        year = text.createMessage(str(slide.datetime)[0:4], text.HEADING, text.GREEN)
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
        showNewSlide()
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def year():
    global showYearState
    showYearState = not showYearState
    if not showYearState:  # Remove the year by redrawing
        screen.displaySurface.fill((0, 0, 0))
        slide = slideshow.getCurrentSlide()
        screen.displaySurface.blit(slide.getSurface(), slide.coordinates())
    showMetaData()


def next():
    showNewSlide()
    if not pauseState:
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def previous():
    showNewSlide(PREVIOUS)
    if not pauseState:
        pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)


def run():
    global pauseState
    global showYearState

    showNewSlide()

    # Creates a periodically repeating event on the event queue
    pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)
    while True:
        event = pygame.event.wait(LOOP_INTERVAL)
        if event.type == pygame.NOEVENT:
            continue
        if event.type == PHOTO_EVENT:
            if not pauseState:
                showNewSlide()
                log.debug(f"Next slide in {PHOTO_INTERVAL} msec")
                pygame.time.set_timer(PHOTO_EVENT, PHOTO_INTERVAL)

        if event.type in [pygame.WINDOWCLOSE, pygame.QUIT]:
            break
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q]:
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

import pygame
from magic_lantern import config

WIDTH, HEIGHT = (1280, 720)


def init():
    global displaySurface
    global WIDTH, HEIGHT

    # pygame setup
    pygame.init()
    print(f"Support for all image formats: {pygame.image.get_extended()}")
    if config.fullscreen:
        displaySurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))

    WIDTH, HEIGHT = displaySurface.get_size()
    pygame.mouse.set_visible(False)


def rect():
    return pygame.Rect(0, 0, WIDTH, HEIGHT)


def size():
    return (WIDTH, HEIGHT)


def aspect():
    return WIDTH / HEIGHT

import pygame

WIDTH, HEIGHT = (1280, 720)


def init():
    global displaySurface
    global WIDTH, HEIGHT

    # pygame setup
    pygame.init()

    displaySurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))

    WIDTH, HEIGHT = displaySurface.get_size()
    pass


def rect():
    return pygame.Rect(0, 0, WIDTH, HEIGHT)


def size():
    return (WIDTH, HEIGHT)


def aspect():
    return WIDTH / HEIGHT

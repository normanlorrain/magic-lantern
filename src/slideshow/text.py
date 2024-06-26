import pygame

font = None


def init():
    global font
    pygame.font.init()
    font = pygame.font.SysFont("freesansbold", 36)
    # fonts = pygame.font.get_fonts()
    # pass


def createMessage(msg):
    textSurface = font.render(msg, True, (0, 255, 0))
    return textSurface

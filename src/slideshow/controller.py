import time
import pygame

from slideshow import album
from slideshow import screen

photoList = []


def init(path):

    screen.init()
    album.init(path)

    # for i in range(3):
    #     photo = album.getNextPhoto()
    #     photoList.append(photo)


def run():
    clock = pygame.time.Clock()

    running = True

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your displaySurface
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.unicode == "q":
                    running = False

        # Blank the screen
        screen.displaySurface.fill((0, 0, 0))
        # for photo in photoList:
        photo = album.getNextPhoto()
        screen.displaySurface.blit(photo.getSurface(), photo.transform())

        # flip() the display to put your work on screen
        print("flip")
        pygame.display.flip()

        # limits FPS to 60
        clock.tick(0.5)
        # time.sleep(1)

    pygame.quit()

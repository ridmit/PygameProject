from collections import deque
from random import randint

import pygame

SIZE = WIDTH, HEIGHT = 600, 600
line = 3
COLOURS = list(map(lambda x: (randint(0, 255), randint(0, 255), randint(0, 255)),
                   range(HEIGHT // line)))


def draw():
    global COLOURS
    COLOURS = COLOURS[1:]
    COLOURS.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    w, h = WIDTH, line
    y = 0
    for color in COLOURS:
        pygame.draw.rect(screen, color, (0, y, w, h))
        y += h


pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Фон")

clock = pygame.time.Clock()
fps = 60


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

import pygame

from Car import Car


class PlayerCar(Car):
    def __init__(self, col, speed, way, h, *args):
        super(PlayerCar, self).__init__(col, speed, way, *args)
        self.rect.y = h - self.rect.height


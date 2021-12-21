import pygame


class Car(pygame.sprite.Sprite):
    def __init__(self, col, speed, way, *args):
        super(Car, self).__init__(*args)
        self.image = pygame.image.load(way)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.col = col
        self.speed = speed
        self.rect.x = 50
        self.rect.y = 0

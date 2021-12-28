import pygame


class EnemyCar(pygame.sprite.Sprite):
    width = 80
    image = pygame.image.load("../images/enemy_car.png")
    image = pygame.transform.scale(image, (
    width, image.get_height() * width // image.get_width()))

    def __init__(self, col, h, speed, fps, *args):
        super(EnemyCar, self).__init__(*args)

        self.width = EnemyCar.width
        self.fps = fps
        self.speed = speed
        self.h = h

        self.image = EnemyCar.image
        self.rect = self.image.get_rect()
        self.rect.x = col * self.width
        self.rect.y = -self.rect.height
        self.size = self.image.get_size()
        self.real_y = self.rect.y

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.real_y += self.speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()

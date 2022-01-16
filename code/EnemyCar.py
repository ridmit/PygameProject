import pygame

from AnimatedSprite import AnimatedSprite


class EnemyCar(AnimatedSprite):
    width = 80

    image = pygame.image.load("../images/enemy_car.png")
    image = pygame.transform.scale(image, (
        width, image.get_height() * width // image.get_width()))

    sheet = pygame.image.load("../images/boom_sheet8x4.png")
    cols, rows = 8, 4

    data = None

    def __init__(self, col, h, my_speed, fps, *groups):
        super(EnemyCar, self).__init__(EnemyCar.sheet, EnemyCar.cols,
                                       EnemyCar.rows, False, *groups)
        self.width = EnemyCar.width
        self.fps = fps
        self.h = h
        self.my_speed = my_speed

        self.image = EnemyCar.image
        self.rect = self.image.get_rect()
        self.rect.x = col * self.width
        self.rect.y = -self.rect.height
        self.size = self.image.get_size()
        self.real_y = self.rect.y

        self.mask = pygame.mask.from_surface(self.image)
        self.alive = True

    def update(self, speed, **kwargs):
        speed = self.my_speed + speed
        self.real_y += speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()
            EnemyCar.data[self.rect.x // EnemyCar.width] = False
        if not self.alive:
            super().update(self.fps, 4)

    def explosion(self):
        EnemyCar.data[self.rect.x // EnemyCar.width] = False
        self.alive = False
        self.my_speed = 0
        self.rect.x -= (EnemyCar.sheet.get_width() // EnemyCar.cols
                        - self.image.get_width()) // 2
        self.rect.y += (self.image.get_height() - EnemyCar.sheet.get_height()
                        // EnemyCar.rows) // 2
        super().update(self.fps, 4)  # Смена картинки

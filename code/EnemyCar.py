import pygame


class EnemyCar(pygame.sprite.Sprite):
    width = 80

    image = pygame.image.load("../images/enemy_car.png")
    image = pygame.transform.scale(image, (
        width, image.get_height() * width // image.get_width()))

    explosion_img = pygame.image.load("../images/boom.png")
    explosion_img = pygame.transform.scale(explosion_img, image.get_size())
    data = None

    def __init__(self, col, h, my_speed, fps, *args):
        super(EnemyCar, self).__init__(*args)

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

    def update(self, speed):
        speed = self.my_speed + speed
        self.real_y += speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()
            EnemyCar.data[self.rect.x // EnemyCar.width] = False

    def explosion(self):
        self.alive = False
        self.image = EnemyCar.explosion_img
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width,
                                self.rect.height)
        self.size = self.image.get_size()
        self.my_speed = 0

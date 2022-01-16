import pygame


class PlayerCar(pygame.sprite.Sprite):
    width = 50
    image = pygame.image.load("../images/player_car.png")
    image = pygame.transform.scale(image, (
        width, image.get_height() * width // image.get_width()))

    shield_img = pygame.image.load("../images/shield.png")
    shield_img.set_alpha(230)
    shield_img = pygame.transform.scale(shield_img,
                                        (image.get_height() + 12,
                                         image.get_height() + 12))
    car_x, car_y = (shield_img.get_width() - image.get_width()) // 2, (
            shield_img.get_height() - image.get_height()) // 2

    shield_img.blit(image, (car_x, car_y))

    def __init__(self, w, h, *args):
        super(PlayerCar, self).__init__(*args)

        self.image = PlayerCar.image
        self.rect = self.image.get_rect()
        self.rect.x = (w - PlayerCar.width) // 2
        self.rect.y = h - self.rect.height - 10
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

        self.running = True
        self.again = False
        self.shield = False

    def update(self, final_window, points, shield, *groups):
        if shield and not self.shield:
            self.with_shield()
        for enemy in groups[-1]:  # enemy sprites
            if enemy.alive and pygame.sprite.collide_mask(self, enemy):
                if shield:
                    self.common_image()
                    shield = False
                    enemy.explosion()
                else:
                    final_window.cycle(points, *groups)
                    self.running = False
                    self.again = final_window.again
        self.shield = shield

    def common_image(self):
        self.image = PlayerCar.image
        self.rect = pygame.Rect(self.rect.x + 22, self.rect.y + 6,
                                self.image.get_width(),
                                self.image.get_height())
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

    def with_shield(self):
        self.image = PlayerCar.shield_img
        self.rect = pygame.Rect(self.rect.x - 22, self.rect.y - 6,
                                self.image.get_width(),
                                self.image.get_height())
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

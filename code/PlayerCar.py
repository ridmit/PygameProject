import pygame


class PlayerCar(pygame.sprite.Sprite):
    size = 80
    image = pygame.image.load("../images/player_car.png")
    image = pygame.transform.scale(image, (size, size))

    def __init__(self, h, *args):
        super(PlayerCar, self).__init__(*args)

        self.image = PlayerCar.image
        self.rect = self.image.get_rect()
        self.rect.x = 360
        self.rect.y = h - self.rect.height
        self.size = self.image.get_size()

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, enemy_sprites):
        for elem in enemy_sprites:
            if pygame.sprite.collide_mask(self, elem):
                print("GameOver")


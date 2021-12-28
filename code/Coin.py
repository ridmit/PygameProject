import pygame


class Coin(pygame.sprite.Sprite):
    cnt = 0
    side = 40
    image = pygame.image.load("../images/coin.png")
    image = pygame.transform.scale(image, (side, side))

    def __init__(self, x, y, fps, speed, h, *groups):
        super(Coin, self).__init__(*groups)
        self.side = Coin.side
        self.fps = fps
        self.speed = speed
        self.h = h

        self.image = Coin.image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y

    def update(self, player_sprite):
        self.real_y += self.speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()
        if pygame.sprite.spritecollideany(self, player_sprite):
            Coin.cnt += 1
            self.kill()

import pygame

from AnimatedSprite import AnimatedSprite


class Coin(AnimatedSprite):
    cnt = 0

    sheet = pygame.image.load("../images/coin_sheet6x1.png")
    sheet = pygame.transform.scale(sheet, (
        sheet.get_width() // 3, sheet.get_height() // 3))
    cols, rows = 6, 1

    def __init__(self, x, y, fps, h, *groups):
        super(Coin, self).__init__(Coin.sheet, Coin.cols, Coin.rows,
                                   True, *groups)
        self.fps = fps
        self.h = h

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, speed, k, player):
        self.real_y += speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()
        if pygame.sprite.collide_mask(self, player):
            Coin.cnt += k
            self.kill()
        super(Coin, self).update(self.fps, 12)
        self.mask = pygame.mask.from_surface(self.image)

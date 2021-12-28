import pygame


class Tile(pygame.sprite.Sprite):
    size = 40
    image = pygame.image.load("../images/tile.jpg")
    image = pygame.transform.scale(image, (size, size))
    cnt = 0

    def __init__(self, x, y, fps, h, *groups):
        super(Tile, self).__init__(*groups)

        self.fps = fps
        self.h = h
        self.tile_size = Tile.size

        self.image = Tile.image
        self.rect = self.image.get_rect()

        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y
        self.real_y = y

    def update(self, speed, *groups):
        self.real_y += speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()
            Tile(self.x, -self.tile_size + self.real_y - self.h, self.fps,
                 self.h, *groups)
            Tile.cnt += 1

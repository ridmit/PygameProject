import pygame


class Bonus(pygame.sprite.Sprite):
    side = 40

    def __init__(self, fps, h, *groups):
        super(Bonus, self).__init__(*groups)
        self.side = Bonus.side
        self.fps = fps
        self.h = h

        self.real_y = None
        self.rect = None

    def update(self, speed):
        self.real_y += speed / self.fps
        self.rect.y = self.real_y // 1
        if self.real_y >= self.h:
            self.kill()


class SpeedYBonus(Bonus):
    image = pygame.image.load("../images/boost_y.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(SpeedYBonus, self).__init__(fps, h, *groups)
        self.image = SpeedYBonus.image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class SlowYBonus(Bonus):
    image = pygame.image.load("../images/slow_y.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(SlowYBonus, self).__init__(fps, h, *groups)
        self.image = SlowYBonus.image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class SpeedXBonus(Bonus):
    image = pygame.image.load("../images/boost_x.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(SpeedXBonus, self).__init__(fps, h, *groups)
        self.image = SpeedXBonus.image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class SlowXBonus(Bonus):
    image = pygame.image.load("../images/slow_x.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(SlowXBonus, self).__init__(fps, h, *groups)
        self.image = SlowXBonus.image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class Blob(Bonus):
    image = pygame.image.load("../images/blob_icon.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(Blob, self).__init__(fps, h, *groups)
        self.image = Blob.image
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class XHalf(Bonus):
    image = pygame.image.load("../images/x0.5.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(XHalf, self).__init__(fps, h, *groups)
        self.image = XHalf.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class X2(Bonus):
    image = pygame.image.load("../images/x2.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(X2, self).__init__(fps, h, *groups)
        self.image = X2.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class X3(Bonus):
    image = pygame.image.load("../images/x3.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(X3, self).__init__(fps, h, *groups)
        self.image = X3.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class Shield(Bonus):
    image = pygame.image.load("../images/shield_icon.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(Shield, self).__init__(fps, h, *groups)
        self.image = Shield.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.real_y = y

        self.mask = pygame.mask.from_surface(self.image)


class Boom(Bonus):
    image = pygame.image.load("../images/boom_icon.png")
    image = pygame.transform.scale(image, (Bonus.side, Bonus.side))

    def __init__(self, x, y, fps, h, *groups):
        super(Boom, self).__init__(fps, h, *groups)
        self.image = Boom.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.real_y = y
        self.mask = pygame.mask.from_surface(self.image)

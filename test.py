import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, loop, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.loop = loop
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.cnt = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, fps, frequency):
        self.cnt += 1
        if self.cnt % frequency == 0:  # Частота смены кадров
            if self.loop:  # Анимированный спрайт зациклен
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            else:
                self.cur_frame += 1
                if self.cur_frame + 1 == len(self.frames):
                    self.kill()
        self.image = self.frames[self.cur_frame]


SIZE = WIDTH, HEIGHT = 600, 600

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Взрыв")

clock = pygame.time.Clock()
fps = 60

all_sprites = pygame.sprite.Group()

sheet = pygame.image.load("images/boom_sheet8x4.png")

boom = AnimatedSprite(sheet, 8, 4, False, all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("blue")
    all_sprites.update(fps, 5)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

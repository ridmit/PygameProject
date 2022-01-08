import pygame

from AnimatedSprite import AnimatedSprite

SIZE = WIDTH, HEIGHT = 600, 600

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Взрыв")

clock = pygame.time.Clock()
fps = 60

all_sprites = pygame.sprite.Group()

sheet = pygame.image.load("images/boom4.png")
sheet = pygame.transform.scale(sheet, (sheet.get_width() * 1.5, sheet.get_height() * 1.5))

boom = AnimatedSprite(sheet, 4, 4, 0, 0, all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("blue")
    all_sprites.update(fps, 80)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

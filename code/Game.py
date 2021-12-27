import pygame
import pygame_gui

from Board import Board
from PlayerCar import PlayerCar


class GameScene:
    def __init__(self):
        self.size = self.w, self.h = 1000, 1000

        self.init_ui()

        self.all_sprites = pygame.sprite.Group()
        self.my_car = PlayerCar(3, 20, "../images/player_car.png", self.h)
        self.all_sprites.add(self.my_car)

        self.board = Board(10, 10)

        self.keys = {
            pygame.K_a: False,
            pygame.K_d: False
        }

        self.clock = pygame.time.Clock()
        self.fps = 60

    def init_ui(self):
        pass

    def cycle(self):
        self.running = True
        self.screen = pygame.display.set_mode(self.size)
        while self.running:
            # time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
                # self.manager.process_events(event)

            if self.keys[pygame.K_d]:
                self.my_car.rect.x += 5
            if self.keys[pygame.K_a]:
                self.my_car.rect.x -= 5

            self.draw()
            # self.manager.update(time_delta)
            # self.manager.draw_ui(self.screen)
            pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        if event.type == pygame.KEYUP:
            self.keys[event.key] = False

    def draw(self):
        self.screen.fill("red")
        self.all_sprites.draw(self.screen)
        self.board.render(self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)

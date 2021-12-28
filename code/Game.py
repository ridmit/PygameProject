from random import randint

import pygame
import time
import pygame_gui

from Board import Board
from PlayerCar import PlayerCar
from Tile import Tile
from EnemyCar import EnemyCar


class GameScene:
    def __init__(self):
        self.size = self.w, self.h = 800, 1000
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.speed = 90.0  # пикселей в секунду

        self.init_ui()

        self.all_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.my_car = PlayerCar(self.h, self.player_sprite)

        for x in range(0, self.w, Tile.size):
            for y in range(-Tile.size, self.h, Tile.size):
                Tile(x, y, self.fps, self.h, self.tile_sprites)

        # self.board = Board(10, 10)
        # self.board.set_view(0, 0, 80)

        self.keys = {
            pygame.K_a: False,
            pygame.K_d: False
        }

    def init_ui(self):
        pass

    def cycle(self):
        self.time_spawn = 0
        self.running = True
        self.screen = pygame.display.set_mode(self.size)
        while self.running:
            # time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
                # self.manager.process_events(event)

            self.speed = min(420, self.speed + 0.1)

            self.spawn_car()

            if self.keys[pygame.K_d]:
                self.my_car.rect.x = min(self.my_car.rect.x + 5,
                                         self.w - self.my_car.rect.width)
            if self.keys[pygame.K_a]:
                self.my_car.rect.x = max(self.my_car.rect.x - 5, 0)

            self.player_sprite.update(self.enemy_sprites)
            self.enemy_sprites.update()
            self.tile_sprites.update(self.speed, self.tile_sprites)
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
        self.screen.fill("black")

        self.tile_sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.enemy_sprites.draw(self.screen)
        # self.board.render(self.screen)

        pygame.display.flip()
        self.clock.tick(self.fps)

    def spawn_car(self):
        if time.time() - self.time_spawn >= 0.5:
            self.time_spawn = time.time()
            car = EnemyCar(randint(0, self.w // 20 - 21), self.h,
                           randint(int(self.speed) - 50, int(self.speed)),
                           self.fps)
            if not pygame.sprite.spritecollideany(car, self.enemy_sprites):
                self.enemy_sprites.add(car)


if __name__ == '__main__':
    game = GameScene()
    game.cycle()

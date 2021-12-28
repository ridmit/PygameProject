from random import randint

import pygame
import time
import pygame_gui

from Board import Board
from PlayerCar import PlayerCar
from Tile import Tile
from EnemyCar import EnemyCar
from Coin import Coin


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
        self.coin_sprites = pygame.sprite.Group()

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

        self.my_font = pygame.font.Font(None, 60)
        self.points = 0

    def init_ui(self):
        pass

    def cycle(self):
        self.car_spawn = 0
        self.coin_spawn = 0
        self.running = True
        self.screen = pygame.display.set_mode(self.size)
        while self.running:
            # time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
                # self.manager.process_events(event)

            self.speed = min(420, self.speed + 0.1)

            self.spawn_car()
            self.spawn_coin()

            if self.keys[pygame.K_d]:
                self.my_car.rect.x = min(self.my_car.rect.x + 5,
                                         self.w - self.my_car.rect.width)
            if self.keys[pygame.K_a]:
                self.my_car.rect.x = max(self.my_car.rect.x - 5, 0)

            self.points = Tile.cnt + Coin.cnt * 200

            self.coin_sprites.update(self.player_sprite)
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
        self.tile_sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.coin_sprites.draw(self.screen)
        self.enemy_sprites.draw(self.screen)
        # self.board.render(self.screen)

        self.points_text = self.my_font.render(str(self.points), True,
                                               "blue")
        self.screen.blit(self.points_text,
                         (self.w - self.points_text.get_width(), 0))
        pygame.display.flip()
        self.clock.tick(self.fps)

    def spawn_car(self):
        if time.time() - self.car_spawn >= 0.5:
            self.car_spawn = time.time()
            car = EnemyCar(randint(0, self.w // 80 - 1), self.h,
                           self.speed * randint(13, 19) // 10,
                           self.fps)
            if not pygame.sprite.spritecollideany(car, self.enemy_sprites):
                self.enemy_sprites.add(car)

    def spawn_coin(self):
        if time.time() - self.coin_spawn >= 0.4:
            self.coin_spawn = time.time()
            Coin(randint(0, self.w - 40), -40, self.fps, self.speed,
                 self.h, self.coin_sprites)


if __name__ == '__main__':
    pygame.init()
    game = GameScene()
    game.cycle()

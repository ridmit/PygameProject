from random import uniform, randint, choice, random

import pygame
import time

from PlayerCar import PlayerCar
from Tile import Tile
from EnemyCar import EnemyCar
from Coin import Coin
from Final import FinalScene
from Bonuses import SpeedYBonus, SlowYBonus, SpeedXBonus, SlowXBonus, Blob
from Bonuses import X2, X3, XHalf, Shield, Boom, Question


class GameScene:
    def __init__(self, login):
        self.size = self.w, self.h = 800, 1000
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.again = True

        self.blob = pygame.image.load("../images/blob.png")
        self.blob = pygame.transform.scale(self.blob, (800, 1000))

        self.my_font = pygame.font.Font(None, 60)
        self.final_window = FinalScene(login)

    def new_game(self):
        Tile.cnt = Coin.cnt = 0
        EnemyCar.data = list(map(lambda x: False, range(10)))

        self.keys = {
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
        self.blob.set_alpha(0)
        self.shield = False
        self.points = 0
        self.k = 1

        self.speed = 130.0  # пикселей в секунду
        self.speed_x = 5
        self.player_sprite = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()

        self.all_bns_sprites = pygame.sprite.Group()

        self.speed_y_bns_sprites = pygame.sprite.Group()
        self.slow_y_bns_sprites = pygame.sprite.Group()

        self.speed_x_bns_sprites = pygame.sprite.Group()
        self.slow_x_bns_sprites = pygame.sprite.Group()

        self.blob_sprites = pygame.sprite.Group()

        self.xhalf_sprites = pygame.sprite.Group()
        self.x2_sprites = pygame.sprite.Group()
        self.x3_sprites = pygame.sprite.Group()

        self.shields_sprites = pygame.sprite.Group()
        self.boom_sprites = pygame.sprite.Group()
        self.qstn_sprites = pygame.sprite.Group()

        self.bonuses = {
            SpeedYBonus: self.speed_y_bns_sprites,
            SlowYBonus: self.slow_y_bns_sprites,
            SpeedXBonus: self.speed_x_bns_sprites,
            SlowXBonus: self.slow_x_bns_sprites,
            Blob: self.blob_sprites,
            X2: self.x2_sprites,
            X3: self.x3_sprites,
            XHalf: self.xhalf_sprites,
            Shield: self.shields_sprites,
            Boom: self.boom_sprites,
            Question: self.qstn_sprites
        }

        self.my_car = PlayerCar(self.w, self.h, self.player_sprite)

        for x in range(0, self.w, Tile.size):
            for y in range(-Tile.size, self.h, Tile.size):
                Tile(x, y, self.fps, self.h, self.tile_sprites)

        self.car_spawn = 0
        self.coin_spawn = 0
        self.bonus_spawn = 0

        self.speed_y_timer = None
        self.slow_y_timer = None

        self.blob_timer = 0
        self.k_timer = None
        self.shield_timer = None
        self.prev = None

    def cycle(self):
        self.new_game()
        self.screen = pygame.display.set_mode(self.size)
        while self.my_car.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.bonuses_check()
            self.speed = min(500, self.speed + 0.1)
            self.spawn_car()
            self.spawn_bonus()
            self.spawn_coin()

            if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
                self.my_car.rect.x = min(self.my_car.rect.x + self.speed_x,
                                         self.w - self.my_car.rect.width)
            if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
                self.my_car.rect.x = max(self.my_car.rect.x - self.speed_x, 0)

            self.points = int(Tile.cnt // 2 + Coin.cnt * 100)
            if time.time() - self.blob_timer > 1:
                self.blob.set_alpha(self.blob.get_alpha() - 1)

            self.update_sprites()
            self.draw()
            self.shield = self.my_car.shield

            pygame.display.flip()
        if self.my_car.again:
            self.cycle()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.my_car.running = False
            self.again = False
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        if event.type == pygame.KEYUP:
            self.keys[event.key] = False

    def update_sprites(self):
        self.coin_sprites.update(self.speed, self.k, self.my_car)
        self.enemy_sprites.update(self.speed)
        self.player_sprite.update(self.final_window,
                                  self.points,
                                  self.shield,
                                  self.tile_sprites,
                                  self.all_bns_sprites,
                                  self.player_sprite,
                                  self.coin_sprites,
                                  self.enemy_sprites)
        self.tile_sprites.update(self.speed, self.k, self.tile_sprites)

        self.all_bns_sprites.update(self.speed)

    def draw(self):
        self.tile_sprites.draw(self.screen)
        self.coin_sprites.draw(self.screen)
        self.all_bns_sprites.draw(self.screen)
        self.enemy_sprites.draw(self.screen)
        self.player_sprite.draw(self.screen)

        self.points_text = self.my_font.render(str(self.points), True, "blue")
        self.screen.blit(self.points_text,
                         (self.w - self.points_text.get_width(), 0))
        self.screen.blit(self.blob, (0, 0))
        pygame.display.flip()
        self.clock.tick(self.fps)

    def spawn_car(self):
        if time.time() - self.car_spawn >= \
                -7 / 18500 * self.speed + 434 / 925 + uniform(-0.08, 0.1):
            self.car_spawn = time.time()
            possible_col = [i for i, elem in enumerate(EnemyCar.data)
                            if not elem]
            if possible_col:
                col = choice(possible_col)
                EnemyCar(col, self.h, 150 * uniform(0.5, 1.7),
                         self.fps, self.enemy_sprites)
                EnemyCar.data[col] = True

    def spawn_coin(self):
        if time.time() - self.coin_spawn >= \
                - 1 / 1480 * self.speed + 361 / 740 + uniform(-0.05, 0.1):
            self.coin_spawn = time.time()
            my_rand = random()
            if my_rand <= 0.40:  # Шанс 40% на спавн 1 монеты
                cnt = 1
            elif my_rand <= 0.75:  # Шанс 35% на спавн 2 монет
                cnt = 2
            else:  # Шанс 25% на спавн 3 монет
                cnt = 3
            for _ in range(cnt):
                coin = Coin(randint(0, self.w - 40), -40, self.fps, self.h)
                if not pygame.sprite.spritecollideany(
                        coin, self.coin_sprites):
                    if not pygame.sprite.spritecollideany(
                            coin, self.all_bns_sprites):
                        self.coin_sprites.add(coin)

    def spawn_bonus(self):
        if time.time() - self.bonus_spawn >= \
                -1 / 740 * self.speed + 236 / 185 + uniform(-0.15, 0.15):
            self.bonus_spawn = time.time()
            cnt = 2 if random() >= 0.8 else 1
            for _ in range(cnt):
                possible_bns = [SpeedYBonus, SlowYBonus, SpeedXBonus,
                                SlowXBonus, Blob, X2, X3, XHalf, Shield,
                                Boom, Question]
                bonus = choice(possible_bns)
                while self.prev == bonus:
                    bonus = choice(possible_bns)
                self.prev = bonus
                x, y = randint(0, self.w - 40), -40
                group = self.bonuses[bonus]
                bonus = bonus(x, y, self.fps, self.h, group)
                if not pygame.sprite.spritecollideany(
                        bonus, self.all_bns_sprites):
                    if not pygame.sprite.spritecollideany(
                            bonus, self.coin_sprites):
                        """
                        Если попался случайный бонус, то рандомно выбираем
                        один из активных бонусов(тех, что легко опознать).
                        """

                        if group == self.qstn_sprites:
                            self.bonuses[choice([Blob,
                                                 Boom,
                                                 Shield])].add(bonus)
                        self.all_bns_sprites.add(bonus)

    def bonuses_check(self):
        now = time.time()
        if pygame.sprite.spritecollide(self.my_car, self.speed_y_bns_sprites,
                                       True):
            self.speed_y_timer = now
            self.speed += 100

        if pygame.sprite.spritecollide(self.my_car, self.slow_y_bns_sprites,
                                       True):
            self.slow_y_timer = now
            self.speed = max(self.speed - 100, 100)

        if pygame.sprite.spritecollide(self.my_car, self.speed_x_bns_sprites,
                                       True):
            self.speed_x += 2

        if pygame.sprite.spritecollide(self.my_car, self.slow_x_bns_sprites,
                                       True):
            self.speed_x = max(self.speed_x - 2, 1)

        if pygame.sprite.spritecollide(self.my_car, self.blob_sprites, True):
            self.blob.set_alpha(255)
            self.blob_timer = now

        if pygame.sprite.spritecollide(self.my_car, self.shields_sprites,
                                       True):
            self.shield = True
            self.shield_timer = now

        if pygame.sprite.spritecollide(self.my_car, self.boom_sprites,
                                       True):
            for enemy in self.enemy_sprites:
                enemy.explosion()

        for group, k in zip(
                [self.xhalf_sprites, self.x2_sprites, self.x3_sprites],
                [0.5, 2, 3]):
            if pygame.sprite.spritecollide(self.my_car, group, True):
                self.k = k
                self.k_timer = now

        if self.speed_y_timer and now - self.speed_y_timer >= 15:
            self.speed -= 100
            self.speed_y_timer = None

        if self.slow_y_timer and now - self.slow_y_timer >= 15:
            self.speed += 100
            self.slow_y_timer = None

        if self.k_timer and now - self.k_timer >= 15:
            self.k = 1
            self.k_timer = None

        if self.shield_timer and now - self.shield_timer >= 20:
            self.shield = False
            self.shield_timer = None
            self.my_car.common_image()


if __name__ == '__main__':
    pygame.init()
    game = GameScene("qwe")
    game.cycle()

import pygame
import pygame_gui

from db_work import from_db
from terminate import terminate


class LeaderboardScene():
    def __init__(self, login):
        self.size = self.w, self.h = 626, 417
        self.image = pygame.image.load("../images/leaderboard.png")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.login = login
        self.init_ui()

        self.font_10 = pygame.font.Font(None, 21)
        self.font_25 = pygame.font.Font(None, 25)

    def init_ui(self):
        self.manager = pygame_gui.UIManager(self.size)

        x, y = 90, 35
        # Кнопки
        self.ok_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.w - x) // 2, self.h - y - 10),
                                      (x, y)),
            text="OK",
            manager=self.manager)

    def cycle(self):
        self.screen = pygame.display.set_mode(self.size)

        data = [[log, points] for _, log, _, points in from_db()]
        self.data = [[i + 1] + elem for i, elem in enumerate(data)
                     if i <= 4 or elem[0] == self.login]

        if len(self.data) == 6:  # Игрок не входит в топ-5
            self.data = self.data[:-2] + self.data[-1:]
        self.draw()

        self.running = True
        while self.running:
            time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ok_btn:
                    self.running = False

    def draw(self):  # Нанесение надписей
        self.screen.blit(self.image, (0, 0))

        x_place, x_nickname, x_points = 153, 250, 490  # x-ы для надписей
        y = 125

        for i, elem in enumerate(self.data):
            place, nick, points = map(str, elem)
            if i == 4:
                self.draw_text(place, x_place, y, self.font_10)
                if place != "5":
                    self.draw_text("...", 355, 292, self.font_25)

            self.draw_text(nick, x_nickname, y, self.font_25)

            text = self.font_25.render(points, True, pygame.Color('white'))
            self.draw_text(points, x_points - text.get_width(), y,
                           self.font_25)

            y += 49

    def draw_text(self, text, x, y, font):
        text = font.render(text, True, pygame.Color('white'))
        rect = text.get_rect()
        rect.left, rect.top = x, y
        self.screen.blit(text, rect)

import pygame
import pygame_gui

from Leaderboard import LeaderboardScene
from db_work import update_points
from terminate import terminate

class FinalScene:
    def __init__(self, login):
        self.size = self.w, self.h = 800, 1000

        self.init_ui()
        self.again = None
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.game_over = pygame.image.load("../images/game_over.png")
        self.login = login
        self.leaderboard = LeaderboardScene(login)

    def init_ui(self):
        self.manager = pygame_gui.UIManager(self.size)

        # Кнопки
        x, y = 200, 40
        self.restart_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.w - x) // 2, 550), (x, y)),
            text="Try again",
            manager=self.manager)
        self.leaderboard_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.w - x) // 2, 650), (x, y)),
            text="Leaderboard",
            manager=self.manager)

    def cycle(self, points, *groups):
        update_points(self.login, points)
        self.screen = pygame.display.set_mode(self.size)
        self.running = True
        while self.running:
            time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
                self.manager.process_events(event)

            for group in groups:
                group.draw(self.screen)
            self.draw()
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.restart_btn:
                    self.running = False
                    self.again = True
                if event.ui_element == self.leaderboard_btn:
                    self.leaderboard.cycle()
                    self.screen = pygame.display.set_mode(self.size)

    def draw(self):
        self.screen.blit(self.game_over,
                         ((self.w - self.game_over.get_width()) // 2, 100))

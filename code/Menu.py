import pygame
import pygame_gui

from Rules import RulesScene
from terminate import terminate


class MenuScene:
    def __init__(self):
        self.size = self.w, self.h = 500, 500

        self.init_ui()

        self.image = pygame.image.load("../images/road.png")
        self.image = pygame.transform.scale(self.image, (520, 520))

        font_50 = pygame.font.Font(None, 50)
        self.title = font_50.render("Final Destination", True, (0, 0, 128))

        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.rules = RulesScene()
        self.res = None

    def init_ui(self):
        self.manager = pygame_gui.UIManager(self.size)

        # Кнопки
        self.start_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.w - 100) // 2, (self.h - 50) // 2 - 70), (100, 50)),
            text="Start game",
            manager=self.manager)
        self.quit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.w - 100) // 2, (self.h - 50) // 2 + 70), (100, 50)),
            text="Quit",
            manager=self.manager)
        self.rules_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.w - 100) // 2,
                                       (self.h - 50) // 2),
                                      (100, 50)),
            text="Rules",
            manager=self.manager)

    def cycle(self):
        self.screen = pygame.display.set_mode(self.size)
        while self.running:
            time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
                self.manager.process_events(event)

            self.draw()
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_btn:
                    self.res = True
                    self.running = False
                if event.ui_element == self.quit_btn:
                    terminate()
                if event.ui_element == self.rules_btn:
                    self.rules.cycle()
                    self.screen = pygame.display.set_mode(self.size)

    def draw(self):  # Нанесение надписей
        self.screen.blit(self.image, (-10, -10))
        self.screen.blit(self.title,
                         ((self.w - self.title.get_width()) // 2, 30))

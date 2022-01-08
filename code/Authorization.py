import pygame
import pygame_gui

from Registration import RegistrationScene
from db_work import from_db


class AuthorizationScene:
    def __init__(self):
        self.size = self.w, self.h = 500, 300
        self.image = pygame.image.load("../images/bgr_authorization.jpg")
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

        self.init_ui()
        self.registration = RegistrationScene()

        self.res, self.login, self.password = False, None, None
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60

    def init_ui(self):
        self.manager = pygame_gui.UIManager(self.size)

        # Шрифты
        font_25 = pygame.font.Font(None, 25)
        # 35 шрифт используется в др методах
        self.font_35 = pygame.font.Font(None, 35)
        font_50 = pygame.font.Font(None, 50)

        # Обычный текст
        self.reg_label = font_25.render("Don't have an account?", True,
                                        "black")
        self.title = font_50.render("Final Destination", True, "black")
        self.log_label = self.font_35.render("Account name", True, "black")
        self.psswd_label = self.font_35.render("Password", True, "black")
        self.status = self.font_35.render("", True, "red")

        x, y = 90, 35
        align, self.dist = 5, 40
        # Кнопки
        self.log_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.w // 2 - x - self.dist, self.h // 2 + y), (x, y)),
            text="LOGIN",
            manager=self.manager)
        self.cancel_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.w // 2 + self.dist, self.h // 2 + y), (x, y)),
            text="CANCEL",
            manager=self.manager)
        self.reg_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.w - self.dist - 190,
                 self.h - self.reg_label.get_height() - self.dist - align),
                (190, 25)),
            text="CREATE A NEW ACCOUNT",
            manager=self.manager)

        dx, dy = 10, 17
        # Поля ввода
        self.log_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.dist + self.log_label.get_width() + dx,
                 self.dist + self.title.get_height() + dy),
                (self.w - self.dist * 2 - self.log_label.get_width() - dx,
                 35)),
            manager=self.manager)
        self.psswd_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.log_text.relative_rect.x, self.log_text.rect.y + 45),
                (self.log_text.relative_rect.width, 35)),
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
            self.running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.log_btn:
                    try_log = str(self.log_text.text)
                    try_pass = str(self.psswd_text.text)
                    for _, log, psswd, _ in from_db():
                        if str(log) == try_log and \
                                str(psswd) == try_pass:
                            self.res, self.login, self.password = True, try_log, try_pass
                            self.running = False
                    self.status = self.font_35.render(
                        "Incorrect username or password", True, "red")
                if event.ui_element == self.cancel_btn:
                    self.running = False
                if event.ui_element == self.reg_btn:
                    self.registration.cycle()
                    self.screen = pygame.display.set_mode(self.size)
                    self.status = self.font_35.render("", True, "red")

    def draw(self):  # Нанесение надписей
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.title,
                         ((self.w - self.title.get_width()) // 2, self.dist))
        self.screen.blit(
            self.log_label,
            (self.dist, self.dist + self.title.get_height() + 20))
        self.screen.blit(
            self.psswd_label,
            (self.dist + self.log_label.get_width() -
             self.psswd_label.get_width(),
             self.log_btn.rect.y - self.psswd_label.get_height() - 20))
        self.screen.blit(self.reg_label, (
            self.dist, self.h - self.reg_label.get_height() - self.dist))
        self.screen.blit(self.status,
                         ((self.w - self.status.get_width()) // 2,
                          self.h - self.status.get_height() - 6))

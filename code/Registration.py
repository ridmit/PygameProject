import pygame
import pygame_gui

from terminate import terminate
from db_work import unique_nick, add_to_db


class RegistrationScene:
    def __init__(self):
        self.size = self.w, self.h = 500, 260
        self.image = pygame.image.load("../images/bgr_reg.jpg")
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

        self.init_ui()
        self.clock = pygame.time.Clock()
        self.fps = 60

    def init_ui(self):
        self.manager = pygame_gui.UIManager(self.size)

        # Шрифты, 30 шрифт используется в других методах
        self.font_30 = pygame.font.Font(None, 30)
        font_45 = pygame.font.Font(None, 45)

        # Обычный текст
        self.title = font_45.render("Registration", True, "black")
        self.log_label = self.font_30.render("Username", True, "black")
        self.psswd_lbl1 = self.font_30.render("Password", True, "black")
        self.psswd_lbl2 = self.font_30.render("Confirm password", True,
                                              "black")
        self.text = self.font_30.render("", True, "red")

        self.dist = 22
        self.distance = self.dist + self.psswd_lbl2.get_width()

        x, y = 90, 35
        self.align = 5
        # Кнопки
        self.sign_in_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.w // 2 - self.dist - x,
                                       self.h - self.dist - y),
                                      (x, y)),
            text="SIGN IN",
            manager=self.manager)
        self.cancel_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.w // 2 + self.dist, self.h - self.dist - y), (x, y)),
            text="CANCEL",
            manager=self.manager)

        # Поля ввода
        self.log_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.distance,
                 self.dist * 2 + self.title.get_height() - self.align),
                (self.w - self.distance - self.dist, y)),
            manager=self.manager)
        self.psswd_text1 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.distance,
                 self.dist * 3 + self.title.get_height() + self.align * 2),
                (self.w - self.distance - self.dist, y)),
            manager=self.manager)
        self.psswd_text2 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.distance,
                 self.dist * 4 + self.title.get_height() + self.align * 5),
                (self.w - self.distance - self.dist, y)),
            manager=self.manager)

    def cycle(self):
        self.running = True
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
                if event.ui_element == self.cancel_btn:
                    self.running = False
                if event.ui_element == self.sign_in_btn:
                    login = str(self.log_text.text)
                    password1 = str(self.psswd_text1.text)
                    password2 = str(self.psswd_text2.text)
                    if "" in [login, password1, password2]:
                        self.text = self.font_30.render(
                            "Enter your login and passwords", True,
                            "red")
                    elif password1 != password2:
                        self.text = self.font_30.render(
                            "Passwords don't match", True, "red")
                    elif not unique_nick(login):
                        self.text = self.font_30.render(
                            f"Username {self.log_text.text} is not available",
                            True, "red")
                    else:
                        add_to_db(login, password1, 0)
                        self.running = False

    def draw(self):  # Нанесение надписей
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.title, ((self.w - self.title.get_width()) // 2,
                                      self.dist))
        self.screen.blit(self.log_label, (
            self.distance - self.log_label.get_width(),
            self.dist * 2 + self.title.get_height()))
        self.screen.blit(
            self.psswd_lbl1,
            (self.distance - self.psswd_lbl1.get_width(),
             self.dist * 3 + self.title.get_height() + self.align * 3))
        self.screen.blit(
            self.psswd_lbl2,
            (self.distance - self.psswd_lbl2.get_width(),
             self.dist * 4 + self.title.get_height() + self.align * 6))
        self.screen.blit(self.text,
                         ((self.w - self.text.get_width()) // 2,
                          self.h - self.dist - self.align * 12))

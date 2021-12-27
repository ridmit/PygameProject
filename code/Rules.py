import pygame
import pygame_gui


class RulesScene:
    def __init__(self):
        self.size = self.w, self.h = 600, 600

        self.init_ui()

        self.image = pygame.image.load("../images/rules.png")
        self.image = pygame.transform.scale(self.image, (320, 130))

        self.clock = pygame.time.Clock()
        self.fps = 60


    def init_ui(self):
        self.manager = pygame_gui.UIManager(self.size)

        self.ok_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.w - 100) // 2, self.h - 20 - 50),
                                      (100, 50)),
            text="OK",
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
            self.running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ok_btn:
                    self.running = False

    def draw(self):
        self.screen.fill("yellow")
        self.screen.blit(self.image,
                         ((self.w - self.image.get_width()) // 2, 20))

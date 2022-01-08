import pygame
import pygame_gui

from terminate import terminate


class RulesScene:
    def __init__(self):
        self.size = self.w, self.h = 800, 900

        self.init_ui()

        self.image = pygame.image.load("../images/rules.png")
        self.image = pygame.transform.scale(self.image, (320, 130))

        self.bgr = pygame.image.load("../images/bgr_rules.jpg")
        self.bgr = pygame.transform.scale(self.bgr, self.size)

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.color = "white"
        self.font_30 = pygame.font.Font(None, 30)
        self.data = [
            "Управляйте машинкой при помощи клавиш 'A' и 'D'",
            "Цель игры - набрать как можно больше очков.",
            "Очки даются за пройденное расстояние и собранные монетки.",
            "Объезжайте препятствия, собирая по пути бонусы и монеты.",
            "Виды бонусов:"]

        self.bns_images_pathes = [
            "../images/boost_y.png",
            "../images/slow_y.png",
            "../images/boost_x.png",
            "../images/slow_x.png",
            "../images/blob_icon.png",
            "../images/shield_icon.png",
            "../images/boom_icon.png",
            "../images/x0.5.png",
            "../images/x2.png",
            "../images/x3.png"]

        self.bns_descriptions = [
            "Ускорение по вертикали на 15 секунд",
            "Замедление по вертикали на 15 секунд",
            "Ускорение по горизонтали",
            "Замедление по горизонтали",
            "Клякса, мешающая обзору и пропадающая через какое-то время",
            "Щит, действующий 20 секунд и защищающий от столкновения",
            "Взрыв всех уже появившихся машин-препятствий",
            "Уменьшение получаемых очков в 2 раза на 15 секунд",
            "Увеличение получаемых очков в 2 раза на 15 секунд",
            "Увеличение получаемых очков в 3 раза на 15 секунд"]

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
        self.draw()
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

    def draw(self):
        self.screen.blit(self.bgr, (0, 0))
        self.screen.blit(self.image,
                         ((self.w - self.image.get_width()) // 2, 20))

        y, interval = 170, 30
        for string in self.data:
            self.draw_text(string, y, self.font_30)
            y += interval

        img_x, img_y = 40, 300
        text_x, text_y = img_x + 70, img_y + 15
        icon_size, interval = 40, 50
        for img_pass, dsc in zip(self.bns_images_pathes,
                                 self.bns_descriptions):
            img = pygame.image.load(img_pass)
            img = pygame.transform.scale(img, (icon_size, icon_size))
            self.screen.blit(img, (img_x, img_y))
            self.draw_desc_text(dsc, text_x, text_y, self.font_30)
            img_y += interval
            text_y += interval

    def draw_text(self, text, y, font):
        text = font.render(text, True, self.color)
        rect = text.get_rect()
        rect.left, rect.top = (self.w - text.get_width()) // 2, y
        self.screen.blit(text, rect)

    # В draw_text для вычисления x нужно знать text.get_width
    # А для этого надо делать font.render() в самой ф-ии
    def draw_desc_text(self, text, x, y, font):
        text = font.render(text, True, self.color)
        rect = text.get_rect()
        rect.left, rect.top = x, y
        self.screen.blit(text, rect)

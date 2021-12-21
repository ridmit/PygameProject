import pygame
import pygame_gui

from Board import Board
from PlayerCar import PlayerCar
from db_work import add_to_db, unique_nick, from_db

SIZE = WIDTH, HEIGHT = 1000, 1000


def authorization():
    size = w, h = 500, 300
    screen = pygame.display.set_mode(size)

    manager = pygame_gui.UIManager(size)

    font_25 = pygame.font.Font(None, 25)
    font_35 = pygame.font.Font(None, 35)
    font_50 = pygame.font.Font(None, 50)
    reg_label = font_25.render("Don't have an account?", True, "black")
    title = font_50.render("Final Destination", True, "black")
    log_label = font_35.render("Account name", True, "black")
    psswd_label = font_35.render("Password", True, "black")

    x, y = 90, 35
    align, dist = 5, 40
    log_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((w // 2 - x - dist, h // 2 + y),
                                  (x, y)),
        text="LOGIN",
        manager=manager)
    cancel_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((w // 2 + dist, h // 2 + y), (x, y)),
        text="CANCEL",
        manager=manager)
    reg_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((w - dist - 190,
                                   h - reg_label.get_height() - dist - align),
                                  (190, 25)),
        text="CREATE A NEW ACCOUNT",
        manager=manager)

    dx, dy = 10, 17
    log_text = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (dist + log_label.get_width() + dx,
             dist + title.get_height() + dy),
            (w - dist * 2 - log_label.get_width() - dx, 35)),
        manager=manager)
    psswd_text = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (log_text.relative_rect.x, log_text.rect.y + 45),
            (log_text.relative_rect.width, 35)),
        manager=manager)

    text = font_35.render("", True, "red")
    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None, None
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == log_btn:
                        try_log = str(log_text.text)
                        try_pass = str(psswd_text.text)
                        for _, log, psswd, _ in from_db():
                            if str(log) == try_log and str(psswd) == try_pass:
                                return True, try_log, try_pass
                        text = font_35.render(
                            "Incorrect username or password", True, "red")
                    if event.ui_element == cancel_btn:
                        return False, None, None
                    if event.ui_element == reg_btn:
                        registration()
                        screen = pygame.display.set_mode(size)
                        text = font_35.render("", True, "red")
            manager.process_events(event)
        manager.update(time_delta)

        screen.fill("green")
        screen.blit(title, ((w - title.get_width()) // 2, dist))
        screen.blit(log_label, (dist, dist + title.get_height() + 20))
        screen.blit(psswd_label,
                    (dist + log_label.get_width() - psswd_label.get_width(),
                     log_btn.rect.y - psswd_label.get_height() - 20))
        screen.blit(reg_label, (dist, h - reg_label.get_height() - dist))
        screen.blit(text, ((w - text.get_width()) // 2,
                           h - text.get_height() - 6))

        manager.draw_ui(screen)
        pygame.display.flip()


def registration():
    size = w, h = 500, 260
    screen = pygame.display.set_mode(size)

    manager = pygame_gui.UIManager(size)

    font_30 = pygame.font.Font(None, 30)
    font_45 = pygame.font.Font(None, 45)
    title = font_45.render("Registration", True, "black")
    log_label = font_30.render("Username", True, "black")
    psswd_lbl1 = font_30.render("Password", True, "black")
    psswd_lbl2 = font_30.render("Confirm password", True, "black")
    dist = 22
    distance = dist + psswd_lbl2.get_width()

    x, y = 90, 35
    align = 5
    sign_in_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((w // 2 - dist - x, h - dist - y), (x, y)),
        text="SIGN IN",
        manager=manager)
    cancel_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((w // 2 + dist, h - dist - y), (x, y)),
        text="CANCEL",
        manager=manager)

    log_text = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (distance, dist * 2 + title.get_height() - align),
            (w - distance - dist, y)),
        manager=manager)
    psswd_text1 = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (distance, dist * 3 + title.get_height() + align * 2),
            (w - distance - dist, y)),
        manager=manager)
    psswd_text2 = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(
            (distance, dist * 4 + title.get_height() + align * 5),
            (w - distance - dist, y)),
        manager=manager)

    text = font_30.render("", True, "red")
    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == cancel_btn:
                        running = False
                    if event.ui_element == sign_in_btn:
                        login = str(log_text.text)
                        password1 = str(psswd_text1.text)
                        password2 = str(psswd_text2.text)
                        if "" in [login, password1, password2]:
                            text = font_30.render(
                                "Enter your login and passwords", True, "red")
                        elif password1 != password2:
                            text = font_30.render("Passwords don't match",
                                                  True, "red")
                        elif not unique_nick(login):
                            text = font_30.render(
                                f"Username {log_text.text} is not available",
                                True, "red")
                        else:
                            add_to_db(login, password1)
                            running = False

            manager.process_events(event)
        manager.update(time_delta)

        screen.fill("purple")
        screen.blit(title, ((w - title.get_width()) // 2, dist))
        screen.blit(log_label, (
            distance - log_label.get_width(), dist * 2 + title.get_height()))
        screen.blit(psswd_lbl1, (distance - psswd_lbl1.get_width(),
                                 dist * 3 + title.get_height() + align * 3))
        screen.blit(psswd_lbl2, (distance - psswd_lbl2.get_width(),
                                 dist * 4 + title.get_height() + align * 6))
        screen.blit(text,
                    ((w - text.get_width()) // 2, h - dist - align * 12))

        manager.draw_ui(screen)
        pygame.display.flip()


def menu(login, password):
    size = w, h = 500, 500
    screen = pygame.display.set_mode(size)

    image = pygame.image.load("../images/road.png")
    image = pygame.transform.scale(image, size)
    font_50 = pygame.font.Font(None, 50)
    title = font_50.render("Final Destination", True, "purple")

    manager = pygame_gui.UIManager(size)

    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            ((w - 100) // 2, (h - 50) // 2 - 70), (100, 50)),
        text="Start game",
        manager=manager)

    quit_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            ((w - 100) // 2, (h - 50) // 2 + 70), (100, 50)),
        text="Quit",
        manager=manager)

    rules_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((w - 100) // 2, (h - 50) // 2), (100, 50)),
        text="Rules",
        manager=manager)

    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_btn:
                        return True
                    if event.ui_element == quit_btn:
                        return False
                    if event.ui_element == rules_btn:
                        rules()
                        screen = pygame.display.set_mode(size)
            manager.process_events(event)

        manager.update(time_delta)
        screen.fill("green")
        screen.blit(image, (0, 0))
        screen.blit(title, ((w - title.get_width()) // 2, 30))
        manager.draw_ui(screen)
        pygame.display.flip()


def rules():
    size = w, h = 600, 600
    screen = pygame.display.set_mode(size)
    image = pygame.image.load("../images/rules.png")
    image = pygame.transform.scale(image, (320, 130))

    manager = pygame_gui.UIManager(size)

    ok_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((w - 100) // 2, h - 20 - 50), (100, 50)),
        text="OK",
        manager=manager)

    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ok_btn:
                        running = False

            manager.process_events(event)
        manager.update(time_delta)
        screen.fill("yellow")
        screen.blit(image, ((w - image.get_width()) // 2, 20))
        manager.draw_ui(screen)

        pygame.display.flip()


def game():
    screen = pygame.display.set_mode(SIZE)

    all_sprites = pygame.sprite.Group()
    my_car = PlayerCar(3, 20, "../images/player_car.png", HEIGHT)
    all_sprites.add(my_car)

    board = Board(10, 10)

    keys = {
        pygame.K_a: False,
        pygame.K_d: False
    }

    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keys[event.key] = True
            if event.type == pygame.KEYUP:
                keys[event.key] = False

        if keys[pygame.K_d]:
            my_car.rect.x += 5
        if keys[pygame.K_a]:
            my_car.rect.x -= 5

        screen.fill("red")
        all_sprites.draw(screen)
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)


pygame.init()

pygame.display.set_caption("Final Destination")
pygame.display.set_icon(pygame.image.load("../images/icon.png"))

clock = pygame.time.Clock()
fps = 60

res, login, password = authorization()
if res:
    if menu(login, password):
        game()
pygame.quit()

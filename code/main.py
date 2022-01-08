import pygame

from Authorization import AuthorizationScene
from Menu import MenuScene
from Game import GameScene

pygame.init()

pygame.display.set_caption("Final Destination")
pygame.display.set_icon(pygame.image.load("../images/icon.png"))

authorization = AuthorizationScene()  # Там вызывается RegistrationScene
menu = MenuScene()  # В меню вызывается RulesScene

authorization.cycle()
game = GameScene(authorization.login)
if authorization.res:
    menu.cycle()
    if menu.res:
        game.cycle()

pygame.quit()

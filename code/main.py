import pygame
import os

from Authorization import AuthorizationScene
from Menu import MenuScene
from Game import GameScene

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (580, 30)
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

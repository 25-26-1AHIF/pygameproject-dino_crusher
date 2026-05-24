import pygame.sysfont


class GameVariables:
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    SQUARE_SIZE = 48
    FPS = 60

    PLAYER_SKIN = "assets/glock2.png"
    POINTS = 0
    MISSLE_SIZE =  32
    MISSLE_COUNT = 0
    SAVED = False
    BULLETS = 0

    FONT_BIG: pygame.font.Font = None
    FONT_MIDDLE: pygame.font.Font = None
    FONT_SMALL: pygame.font.Font = None

    CLOCK = None
    FPS_VISIBLE = True

    @staticmethod
    def init():
        pygame.init()
        GameVariables.FONT_BIG = pygame.sysfont.SysFont("arial", 70, bold=True)
        GameVariables.FONT_MIDDLE = pygame.sysfont.SysFont("arial", 40, bold=True)
        GameVariables.FONT_SMALL = pygame.sysfont.SysFont("arial", 25, bold=False)




class GameScreens:
    MAIN = "main"
    PLAY = "play"
    EXIT = "exit"
    SETTINGS = "Settings"
    DEAD = "dead"
    INV = "inventory"
    HIGH = "highscores"
    actual_screen = MAIN


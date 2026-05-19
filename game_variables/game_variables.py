import pygame.sysfont


class GameVariables:
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    SQUARE_SIZE = 48
    FPS = 60

    MISSLE_SIZE =  32

    FONT_BIG: pygame.font.Font = None
    FONT_MIDDLE: pygame.font.Font = None
    DONT_SMALL: pygame.font.Font = None

    CLOCK = None

    @staticmethod
    def init():
        pygame.init()
        GameVariables.FONT_BIG = pygame.sysfont.SysFont("arial", 70, bold=True)
        GameVariables.FONT_MIDDLE = pygame.sysfont.SysFont("arial", 40, bold=False)
        GameVariables.FONT_SMALL = pygame.sysfont.SysFont("arial", 14, bold=False)


class GameScreens:
    MAIN = "main"
    PLAY = "play"
    EXIT = "exit"
    actual_screen = MAIN


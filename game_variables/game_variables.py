import pygame.sysfont


class GameVariables:
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    SQUARE_SIZE = 48
    FPS = 60

    PLAYER_SKIN = "assets/glock2.png"
    PLAYER_SKIN_AK = "assets/ak47_1.png"
    POINTS = 0
    MISSLE_SIZE =  32
    MISSLE_COUNT = 0
    SAVED = False
    BULLETS = 0
    MUSIC_TRACK = 1
    DIFFICULTY_P = "none"
    DIFFICULTY_H = "none"
    DIFFICULTY_PFAD = "none"
    COINS = 0
    OWNED_SKINS = ["assets/glock2.png", "assets/ak47_1.png"]
    FONT_BIG: pygame.font.Font = None
    FONT_MIDDLE: pygame.font.Font = None
    FONT_SMALL: pygame.font.Font = None
    ENEMYS_KILLED = 0
    CLOCK = None
    FPS_VISIBLE = True
    MAX_BULLETS = 30
    TOLERANCE = 15
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
    DIFF_P = "difficulty_play"
    DIFF_H = "difficulty_highscore"
    SHOP = "shop"
    actual_screen = MAIN


import  pygame
import json
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens
from game_variables.player import Player
from game_variables.raptor_enemy import Raptor
from game_variables.fly_enemy import Fly



def main_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    titel_text = GameVariables.FONT_BIG.render("Dino-Crusher", True, "limegreen")
    starten_text = GameVariables.FONT_MIDDLE.render("Starten", True, "darkgreen")
    quit_text = GameVariables.FONT_MIDDLE.render("Exit", True, "darkred")
    settings_text = GameVariables.FONT_MIDDLE.render("Settings", True, "darkorange")
    inv_text = GameVariables.FONT_MIDDLE.render("Inventar", True, "gold")
    high_text = GameVariables.FONT_MIDDLE.render("Highscores", True, "darkblue")
    shop_text = GameVariables.FONT_MIDDLE.render("Shop", True, "silver")

    high_text_rect = high_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 300))
    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    starten_text_rect = starten_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 200))
    quit_text_rect = quit_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 680))
    settings_text_rect = settings_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 400))
    inv_text_rect = inv_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 500))
    shop_text_rect = shop_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 590))

    background = pygame.image.load("assets/background.png").convert() #chatgpt für einzeigen von Hintergrund verwendet.
    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if starten_text_rect.collidepoint(event.pos):
                    return GameScreens.DIFF_P
                if quit_text_rect.collidepoint(event.pos):
                    return GameScreens.EXIT
                if settings_text_rect.collidepoint(event.pos):
                    return GameScreens.SETTINGS
                if inv_text_rect.collidepoint(event.pos):
                    return GameScreens.INV
                if high_text_rect.collidepoint(event.pos):
                    return GameScreens.DIFF_H
                if shop_text_rect.collidepoint(event.pos):
                    return GameScreens.SHOP

        screen.blit(background, (0, 0))
        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=quit_text, dest=quit_text_rect)
        screen.blit(source=settings_text, dest=settings_text_rect)
        screen.blit(source=inv_text, dest=inv_text_rect)
        screen.blit(source=high_text, dest=high_text_rect)
        screen.blit(source=shop_text, dest=shop_text_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()




def play_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:

    pygame.display.set_caption("Play Screen")
    player = Player(screen, pfad=GameVariables.PLAYER_SKIN)
    raptor = Raptor(screen)
    fly = Fly(screen)
    fly2 = Fly(screen)
    raptor_rect = pygame.Rect(900, player.y_pos + GameVariables.SQUARE_SIZE - 200, 400, 200)
    fly_rect = pygame.Rect(900, 100, 50, 50)
    fly2_rect = pygame.Rect(0, 100, 50, 50)
    background = pygame.image.load("assets/map.png").convert()

    running = True
#
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = pygame.mouse.get_pos()
                GameVariables.BULLETS = player.shoot(mx, my)
                if GameVariables.ENEMYS_KILLED <= GameVariables.TOLERANCE:
                    player.glock.shoot()
                elif GameVariables.ENEMYS_KILLED > GameVariables.TOLERANCE:
                    player.ak.shoot()

                GameVariables.MISSLE_COUNT += 1

        screen.fill("black")
        screen.blit(background, (0, 0))
        dmg, points_raptor = raptor.draw(screen, raptor_rect.x, raptor_rect.y, my_rect=raptor_rect, missles=player.missles)
        dmg_fly, points_fly = fly.draw(screen, fly_rect.x, fly_rect.y, my_rect=fly_rect, missles=player.missles)
        dmg_fly2, points_fly2 = fly2.draw(screen, fly2_rect.x, fly2_rect.y, my_rect=fly2_rect, missles=player.missles)
        GameVariables.POINTS = points_raptor + points_fly + points_fly2
        points_text = GameVariables.FONT_SMALL.render(f"Points: {GameVariables.POINTS}", True, "gold")
        if GameVariables.ENEMYS_KILLED <= GameVariables.TOLERANCE:
            GameVariables.MAX_BULLETS = 30
        if GameVariables.ENEMYS_KILLED > GameVariables.TOLERANCE:
            GameVariables.MAX_BULLETS = 50
        bullets_text = GameVariables.FONT_SMALL.render(f"Bullets fired: {GameVariables.BULLETS}/{GameVariables.MAX_BULLETS}", True, "gold")
        points_text_rect = points_text.get_rect(center=(GameVariables.SCREEN_WIDTH -75, 25))
        bullets_text_rect = bullets_text.get_rect(center=(GameVariables.SCREEN_WIDTH -100, 50))
        screen.blit(source=points_text, dest=points_text_rect)
        screen.blit(source=bullets_text, dest=bullets_text_rect)
        dead = player.update_and_draw(dmg, dmg_fly, dmg_fly2)
        player_rect = pygame.Rect(player.x_pos, player.y_pos, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)
        raptor.update(raptor_rect, player_rect)
        fly.update(fly_rect, player_rect)
        fly2.update(fly2_rect, player_rect)
        if dead == "dead":
            return GameScreens.DEAD

        # habe ich gesucht wie man die fps sehen kann
        if GameVariables.FPS_VISIBLE:
            fps_text = GameVariables.FONT_SMALL.render(f"FPS: {int(clock.get_fps())}", True, "white")
            screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        clock.tick(GameVariables.FPS)

    pygame.quit()

def settings(screen: pygame.Surface, clock: pygame.time.Clock) -> None:

    fps_on = GameVariables.FONT_MIDDLE.render("FPS: ON", True, "green")
    fps_off = GameVariables.FONT_MIDDLE.render("FPS: OFF", True, "red")
    song1_text = GameVariables.FONT_MIDDLE.render("Song: Expeditionary", True, "white")
    song2_text = GameVariables.FONT_MIDDLE.render("Song: Strength of the Titans", True, "white")
    song3_text = GameVariables.FONT_MIDDLE.render("Song: Linked", True, "white")

    settings_screen = pygame.image.load(
        "assets/background.png").convert()  # chatgpt für einzeigen von Hintergrund verwendet.

    fps_on_rect = fps_on.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    fps_off_rect = fps_off.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    song1_rect = song1_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 200))
    song2_rect = song2_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 280))
    song3_rect = song3_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 360))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fps_on_rect.collidepoint(event.pos):
                    GameVariables.FPS_VISIBLE = not GameVariables.FPS_VISIBLE

                if song1_rect.collidepoint(event.pos): # um musiken zu verwenden habe ich claude verwendet
                    GameVariables.MUSIC_TRACK = 1
                    pygame.mixer.music.load("assets/Expeditionary.mp3")
                    pygame.mixer.music.play(-1)
                if song2_rect.collidepoint(event.pos):
                    GameVariables.MUSIC_TRACK = 2
                    pygame.mixer.music.load("assets/Strength of the Titans.mp3")
                    pygame.mixer.music.play(-1)
                if song3_rect.collidepoint(event.pos):
                    GameVariables.MUSIC_TRACK = 3
                    pygame.mixer.music.load("assets/Jim Yosef, Anna Yvette - Linked [NCS Release].mp3")
                    pygame.mixer.music.play(-1)

        screen.blit(settings_screen, (0, 0))
        if GameVariables.FPS_VISIBLE == True:
            screen.blit(source=fps_on, dest=fps_on_rect)
        else:
            screen.blit(source=fps_off, dest=fps_off_rect)

        if GameVariables.MUSIC_TRACK == 1:
            song1_text = GameVariables.FONT_MIDDLE.render("Song: Expeditionary", True, "green")
            song2_text = GameVariables.FONT_MIDDLE.render("Song: Strength of the Titans", True, "white")
            song3_text = GameVariables.FONT_MIDDLE.render("Song: Linked", True, "white")
        elif GameVariables.MUSIC_TRACK == 2:
            song1_text = GameVariables.FONT_MIDDLE.render("Song: Expeditionary", True, "white")
            song2_text = GameVariables.FONT_MIDDLE.render("Song: Strength of the Titans", True, "green")
            song3_text = GameVariables.FONT_MIDDLE.render("Song: Linked", True, "white")
        else:
            song1_text = GameVariables.FONT_MIDDLE.render("Song: Expeditionary", True, "white")
            song2_text = GameVariables.FONT_MIDDLE.render("Song: Strength of the Titans", True, "white")
            song3_text = GameVariables.FONT_MIDDLE.render("Song: Linked", True, "green")

        screen.blit(song1_text, song1_rect)
        screen.blit(song2_text, song2_rect)
        screen.blit(song3_text, song3_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)

def dead_screen(screen: pygame.Surface, clock: pygame.time.Clock, points):
    died_text = GameVariables.FONT_BIG.render("You died", True, "darkred")
    points_text = GameVariables.FONT_MIDDLE.render(f"Points: {points}", True, "darkred")
    died_text_rect = died_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 250))
    points_text_rect = points_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 400))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN

        screen.fill("black")
        screen.blit(source=died_text, dest=died_text_rect)
        screen.blit(source=points_text, dest=points_text_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)



def inventar(screen: pygame.Surface, clock: pygame.time.Clock):

    running = True
    background = pygame.image.load("assets/background.png").convert()
    skin1 = pygame.image.load("assets/glock2.png").convert_alpha()      # ki für convert alpha verwendet
    skin2 = pygame.image.load("assets/glock3.png").convert_alpha()
    skin3 = pygame.image.load("assets/glock4.png").convert_alpha()
    skin4 = pygame.image.load("assets/glock5.png").convert_alpha()
    skin1 = pygame.transform.scale(skin1, (120, 120))
    skin2 = pygame.transform.scale(skin2, (120, 120))       # google verwendet wie man das bild skaliert
    skin3 = pygame.transform.scale(skin3, (120, 120))
    skin4 = pygame.transform.scale(skin4, (120, 120))
    skin1_rect = skin1.get_rect(center=(200, 200))
    skin2_rect = skin2.get_rect(center=(450, 200))
    skin3_rect = skin3.get_rect(center=(700, 200))
    skin4_rect = skin4.get_rect(center=(950, 200))

    skin5 = pygame.image.load("assets/ak47_1.png").convert_alpha()
    skin6 = pygame.image.load("assets/ak47_2.png").convert_alpha()
    skin7 = pygame.image.load("assets/ak47_3.png").convert_alpha()
    skin8 = pygame.image.load("assets/ak47_4.png").convert_alpha()
    skin9 = pygame.image.load("assets/ak_flipped_transparent.png").convert_alpha()

    skin5 = pygame.transform.scale(skin5, (240, 120))
    skin6 = pygame.transform.scale(skin6, (240, 120))
    skin7 = pygame.transform.scale(skin7, (240, 120))
    skin8 = pygame.transform.scale(skin8, (240, 120))
    skin9 = pygame.transform.scale(skin9, (240, 120))
    skin5_rect = skin5.get_rect(center=(170, 400))
    skin6_rect = skin6.get_rect(center=(420, 400))
    skin7_rect = skin7.get_rect(center=(670, 400))
    skin8_rect = skin8.get_rect(center=(920, 400))
    skin9_rect = skin9.get_rect(center=(170, 520))

    while running:

        screen.blit(background, (0, 0))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skin1_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN = "assets/glock2.png"
                if skin2_rect.collidepoint(event.pos):
                    if "assets/glock3.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN = "assets/glock3.png"
                if skin3_rect.collidepoint(event.pos):
                    if "assets/glock4.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN = "assets/glock4.png"
                if skin4_rect.collidepoint(event.pos):
                    if "assets/glock5.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN = "assets/glock5.png"
                if skin5_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN_AK = "assets/ak47_1.png"
                if skin6_rect.collidepoint(event.pos):
                    if "assets/ak47_2.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN_AK = "assets/ak47_2.png"
                if skin7_rect.collidepoint(event.pos):
                    if "assets/ak47_3.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN_AK = "assets/ak47_3.png"
                if skin8_rect.collidepoint(event.pos):
                    if "assets/ak47_4.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN_AK = "assets/ak47_4.png"
                if skin9_rect.collidepoint(event.pos):
                    if "assets/ak_flipped_transparent.png" in GameVariables.OWNED_SKINS:
                        GameVariables.PLAYER_SKIN_AK = "assets/ak_flipped_transparent.png"

        screen.blit(skin1, skin1_rect)
        if "assets/glock3.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin2, skin2_rect)
        if "assets/glock4.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin3, skin3_rect)
        if "assets/glock5.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin4, skin4_rect)

        screen.blit(skin5, skin5_rect)
        if "assets/ak47_2.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin6, skin6_rect)
        if "assets/ak47_3.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin7, skin7_rect)
        if "assets/ak47_4.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin8, skin8_rect)
        if "assets/ak_flipped_transparent.png" in GameVariables.OWNED_SKINS:
            screen.blit(skin9, skin9_rect)

        if GameVariables.PLAYER_SKIN == "assets/glock2.png":
            pygame.draw.rect(surface=screen,rect=(skin1_rect.inflate(10, 10)), color="white", width=3)    # ki für inflate weil schöner
        if GameVariables.PLAYER_SKIN == "assets/glock3.png":
            pygame.draw.rect(surface=screen, rect=(skin2_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN == "assets/glock4.png":
            pygame.draw.rect(surface=screen,rect=(skin3_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN == "assets/glock5.png":
            pygame.draw.rect(surface=screen,rect=(skin4_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_1.png":
            pygame.draw.rect(surface=screen,rect=(skin5_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_2.png":
            pygame.draw.rect(surface=screen, rect=(skin6_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_3.png":
            pygame.draw.rect(surface=screen,rect=(skin7_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_4.png":
            pygame.draw.rect(surface=screen,rect=(skin8_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak_flipped_transparent.png":
            pygame.draw.rect(surface=screen,rect=(skin9_rect.inflate(20, 10)), color="white", width=3)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)

def highscore(screen: pygame.Surface, clock: pygame.time.Clock):
    hs_text = GameVariables.FONT_BIG.render("Highscores", True, "darkblue")
    hs_text_rect = hs_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    background = pygame.image.load("assets/background.png").convert()

    running = True
    while running:
        screen.blit(background, (0, 0))
        highscores = []
        with open("game_variables/highscore_easy.json", "r") as fp:
            inhalt = json.load(fp)
            for high in inhalt:
                highscores.append(high)

        stoppen = False
        while stoppen == False:
            stoppen = True
            for index in range(len(highscores) - 1):
                element = highscores[index]
                element_next = highscores[index + 1]
                if element < element_next:
                    highscores[index] = element_next
                    highscores[index + 1] = element
                    stoppen = False

        for idx, hs in enumerate(highscores[:5]):
            highs = GameVariables.FONT_MIDDLE.render(f"{idx+1}.             {hs}", True, "darkblue")
            highs_rect = highs.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 200 + idx*100))
            screen.blit(source=highs, dest=highs_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.DIFF_H
        screen.blit(source=hs_text, dest=hs_text_rect)

        pygame.display.flip()
        clock.tick(GameVariables.FPS)


def difficulty_play(screen: pygame.Surface, clock: pygame.time.Clock):
    diff_text = GameVariables.FONT_BIG.render("choose difficulty", True, "limegreen")
    easy_text = GameVariables.FONT_MIDDLE.render("easy", True, "darkgreen")
    middle_text = GameVariables.FONT_MIDDLE.render("middle", True, "gold")
    hard_text = GameVariables.FONT_MIDDLE.render("hard", True, "darkred")
    imp_text = GameVariables.FONT_MIDDLE.render("impossible", True, "purple")
    diff_text_rect = diff_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    easy_text_rect = easy_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 200))
    middle_text_rect = middle_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 300))
    hard_text_rect = hard_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 400))
    imp_text_rect = imp_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 500))
    background = pygame.image.load("assets/background.png").convert()

    running = True
    while running:
        screen.blit(background, (0, 0))
        stoppen = False
        while stoppen == False:
            stoppen = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_P = "easy"
                    return GameScreens.PLAY
                if middle_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_P = "middle"
                    return GameScreens.PLAY
                if hard_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_P = "hard"
                    return GameScreens.PLAY
                if imp_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_P = "impossible"
                    return GameScreens.PLAY

        screen.blit(source=diff_text, dest=diff_text_rect)
        screen.blit(source=easy_text, dest=easy_text_rect)
        screen.blit(source=middle_text, dest=middle_text_rect)
        screen.blit(source=hard_text, dest=hard_text_rect)
        screen.blit(source=imp_text, dest=imp_text_rect)

        pygame.display.flip()
        clock.tick(GameVariables.FPS)

def difficulty_high(screen: pygame.Surface, clock: pygame.time.Clock):
    diff_text = GameVariables.FONT_BIG.render("choose difficulty", True, "darkblue")
    easy_text = GameVariables.FONT_MIDDLE.render("easy", True, "darkblue")
    middle_text = GameVariables.FONT_MIDDLE.render("middle", True, "darkblue")
    hard_text = GameVariables.FONT_MIDDLE.render("hard", True, "darkblue")
    imp_text = GameVariables.FONT_MIDDLE.render("impossible", True, "darkblue")
    diff_text_rect = diff_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    easy_text_rect = easy_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 200))
    middle_text_rect = middle_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 300))
    hard_text_rect = hard_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 400))
    imp_text_rect = imp_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 500))
    background = pygame.image.load("assets/background.png").convert()

    running = True
    while running:
        screen.blit(background, (0, 0))
        stoppen = False
        while stoppen == False:
            stoppen = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_H = "easy"
                    GameVariables.DIFFICULTY_PFAD = "highscore_easy.json"
                    return GameScreens.HIGH
                if middle_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_H = "middle"
                    GameVariables.DIFFICULTY_PFAD = "highscore_middle.json"
                    return GameScreens.HIGH
                if hard_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_H = "hard"
                    GameVariables.DIFFICULTY_PFAD = "highscore_hard.json"
                    return GameScreens.HIGH
                if imp_text_rect.collidepoint(event.pos):
                    GameVariables.DIFFICULTY_H = "impossible"
                    GameVariables.DIFFICULTY_PFAD = "highscore_impossible.json"
                    return GameScreens.HIGH

        screen.blit(source=diff_text, dest=diff_text_rect)
        screen.blit(source=easy_text, dest=easy_text_rect)
        screen.blit(source=middle_text, dest=middle_text_rect)
        screen.blit(source=hard_text, dest=hard_text_rect)
        screen.blit(source=imp_text, dest=imp_text_rect)

        pygame.display.flip()
        clock.tick(GameVariables.FPS)


def save_game():
    with open("game_variables/weapons_coins_save.json", "w") as fp:
        json.dump({"coins": GameVariables.COINS, "owned_skins": GameVariables.OWNED_SKINS}, fp, indent=2)


def shop(screen: pygame.Surface, clock: pygame.time.Clock):
    prize1 = GameVariables.FONT_SMALL.render("500", True, "gold")
    prize2 = GameVariables.FONT_SMALL.render("1000", True, "gold")
    prize3 = GameVariables.FONT_SMALL.render("2000", True, "gold")
    prize5 = GameVariables.FONT_SMALL.render("12000", True, "gold")
    prize6 = GameVariables.FONT_SMALL.render("18000", True, "gold")
    prize7 = GameVariables.FONT_SMALL.render("25000", True, "gold")
    prize8 = GameVariables.FONT_SMALL.render("30000", True, "gold")

    prize1_rect = prize1.get_rect(center=(450, 275))
    prize2_rect = prize2.get_rect(center=(700, 275))
    prize3_rect = prize3.get_rect(center=(950, 275))
    prize5_rect = prize5.get_rect(center=(420, 475))
    prize6_rect = prize6.get_rect(center=(670, 475))
    prize7_rect = prize7.get_rect(center=(920, 475))
    prize8_rect = prize8.get_rect(center=(170, 675))

    running = True
    background = pygame.image.load("assets/background.png").convert()
    skin1 = pygame.image.load("assets/glock2.png").convert_alpha()
    skin2 = pygame.image.load("assets/glock3.png").convert_alpha()
    skin3 = pygame.image.load("assets/glock4.png").convert_alpha()
    skin4 = pygame.image.load("assets/glock5.png").convert_alpha()
    skin1 = pygame.transform.scale(skin1, (120, 120))
    skin2 = pygame.transform.scale(skin2, (120, 120))
    skin3 = pygame.transform.scale(skin3, (120, 120))
    skin4 = pygame.transform.scale(skin4, (120, 120))
    skin1_rect = skin1.get_rect(center=(200, 200))
    skin2_rect = skin2.get_rect(center=(450, 200))
    skin3_rect = skin3.get_rect(center=(700, 200))
    skin4_rect = skin4.get_rect(center=(950, 200))

    skin5 = pygame.image.load("assets/ak47_1.png").convert_alpha()
    skin6 = pygame.image.load("assets/ak47_2.png").convert_alpha()
    skin7 = pygame.image.load("assets/ak47_3.png").convert_alpha()
    skin8 = pygame.image.load("assets/ak47_4.png").convert_alpha()
    skin9 = pygame.image.load("assets/ak_flipped_transparent.png").convert_alpha()

    skin5 = pygame.transform.scale(skin5, (240, 120))
    skin6 = pygame.transform.scale(skin6, (240, 120))
    skin7 = pygame.transform.scale(skin7, (240, 120))
    skin8 = pygame.transform.scale(skin8, (240, 120))
    skin9 = pygame.transform.scale(skin9, (240, 120))
    skin5_rect = skin5.get_rect(center=(170, 400))
    skin6_rect = skin6.get_rect(center=(420, 400))
    skin7_rect = skin7.get_rect(center=(670, 400))
    skin8_rect = skin8.get_rect(center=(920, 400))
    skin9_rect = skin9.get_rect(center=(170, 600))

    while running:

        screen.blit(background, (0, 0))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return GameScreens.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if skin1_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN = "assets/glock2.png"
                if skin2_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN = "assets/glock3.png"
                if skin3_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN = "assets/glock4.png"
                if skin4_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN = "assets/glock5.png"
                if skin5_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN_AK = "assets/ak47_1.png"
                if skin6_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN_AK = "assets/ak47_2.png"
                if skin7_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN_AK = "assets/ak47_3.png"
                if skin8_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN_AK = "assets/ak47_4.png"
                if skin9_rect.collidepoint(event.pos):
                    GameVariables.PLAYER_SKIN_AK = "assets/ak_flipped_transparent.png"

                if prize1_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 500 and "assets/glock3.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 500
                        GameVariables.OWNED_SKINS.append("assets/glock3.png")
                        save_game()
                if prize2_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 1000 and "assets/glock4.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 1000
                        GameVariables.OWNED_SKINS.append("assets/glock4.png")
                        save_game()
                if prize3_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 2000 and "assets/glock5.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 2000
                        GameVariables.OWNED_SKINS.append("assets/glock5.png")
                        save_game()
                if prize5_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 12000 and "assets/ak47_3.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 12000
                        GameVariables.OWNED_SKINS.append("assets/ak47_3.png")
                        save_game()
                if prize6_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 18000 and "assets/ak47_4.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 18000
                        GameVariables.OWNED_SKINS.append("assets/ak47_4.png")
                        save_game()
                if prize7_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 25000 and "assets/ak_flipped_transparent.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 25000
                        GameVariables.OWNED_SKINS.append("assets/ak_flipped_transparent.png")
                        save_game()
                if prize8_rect.collidepoint(event.pos):
                    if GameVariables.COINS >= 30000 and "assets/ak_skin_flipped.png" not in GameVariables.OWNED_SKINS:
                        GameVariables.COINS -= 30000
                        GameVariables.OWNED_SKINS.append("assets/ak_skin_flipped.png")
                        save_game()

        # coins_text im loop neu rendern damit er sich sofort aktualisiert
        coins_text = GameVariables.FONT_SMALL.render(f"Coins: {GameVariables.COINS}", True, "gold")
        coins_rect = coins_text.get_rect(center=(GameVariables.SCREEN_WIDTH - 75, 10))

        # preisfarben: gruen wenn schon gekauft, gold wenn man sich leisten kann, rot wenn zu wenig coins
        def prize_color(price, skin_path): # claude für kürzere version
            if skin_path in GameVariables.OWNED_SKINS:
                return "limegreen"
            elif GameVariables.COINS >= price:
                return "gold"
            else:
                return "red"

        prize1 = GameVariables.FONT_SMALL.render("500", True, prize_color(500, "assets/glock3.png"))
        prize2 = GameVariables.FONT_SMALL.render("1000", True, prize_color(1000, "assets/glock4.png"))
        prize3 = GameVariables.FONT_SMALL.render("2000", True, prize_color(2000, "assets/glock5.png"))
        prize5 = GameVariables.FONT_SMALL.render("12000", True, prize_color(12000, "assets/ak47_3.png"))
        prize6 = GameVariables.FONT_SMALL.render("18000", True, prize_color(18000, "assets/ak47_4.png"))
        prize7 = GameVariables.FONT_SMALL.render("25000", True, prize_color(25000, "assets/ak_flipped_transparent.png"))
        prize8 = GameVariables.FONT_SMALL.render("30000", True, prize_color(30000, "assets/ak_skin_flipped.png"))

        screen.blit(skin1, skin1_rect)
        screen.blit(skin2, skin2_rect)
        screen.blit(skin3, skin3_rect)
        screen.blit(skin4, skin4_rect)

        screen.blit(skin5, skin5_rect)
        screen.blit(skin6, skin6_rect)
        screen.blit(skin7, skin7_rect)
        screen.blit(skin8, skin8_rect)
        screen.blit(skin9, skin9_rect)

        screen.blit(prize1, prize1_rect)
        screen.blit(prize2, prize2_rect)
        screen.blit(prize3, prize3_rect)
        screen.blit(prize5, prize5_rect)
        screen.blit(prize6, prize6_rect)
        screen.blit(prize7, prize7_rect)
        screen.blit(prize8, prize8_rect)

        screen.blit(coins_text, coins_rect)

        if GameVariables.PLAYER_SKIN == "assets/glock2.png":
            pygame.draw.rect(surface=screen,rect=(skin1_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN == "assets/glock3.png":
            pygame.draw.rect(surface=screen, rect=(skin2_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN == "assets/glock4.png":
            pygame.draw.rect(surface=screen,rect=(skin3_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN == "assets/glock5.png":
            pygame.draw.rect(surface=screen,rect=(skin4_rect.inflate(10, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_1.png":
            pygame.draw.rect(surface=screen,rect=(skin5_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_2.png":
            pygame.draw.rect(surface=screen, rect=(skin6_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_3.png":
            pygame.draw.rect(surface=screen,rect=(skin7_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak47_4.png":
            pygame.draw.rect(surface=screen,rect=(skin8_rect.inflate(20, 10)), color="white", width=3)
        if GameVariables.PLAYER_SKIN_AK == "assets/ak_flipped_transparent.png":
            pygame.draw.rect(surface=screen,rect=(skin9_rect.inflate(20, 10)), color="white", width=3)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)


def main():
    GameVariables.init()

    with open("game_variables/weapons_coins_save.json", "r") as fp:
        save_data = json.load(fp)
    GameVariables.COINS = save_data["coins"]
    GameVariables.OWNED_SKINS = save_data["owned_skins"]

    pygame.display.set_caption("Dino Crusher")
    screen = pygame.display.set_mode((GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    main_screen(screen, clock)

    while True:
        if GameScreens.actual_screen == GameScreens.MAIN:
            GameVariables.ENEMYS_KILLED = 0
            screen.fill("black")
            GameScreens.actual_screen = main_screen(screen, clock)
        elif GameScreens.actual_screen == GameScreens.PLAY:
            GameVariables.MISSLE_COUNT = 0
            GameScreens.actual_screen = play_screen(screen, clock)
        elif GameScreens.actual_screen == GameScreens.SETTINGS:
            GameScreens.actual_screen = settings(screen, clock)
        elif GameScreens.actual_screen == GameScreens.EXIT:
            break
        elif GameScreens.actual_screen == GameScreens.DEAD:
            if not GameVariables.SAVED:
                with open("game_variables/highscore_easy.json", "r") as fp:
                    inhalt = json.load(fp)
                    inhalt.append(GameVariables.POINTS)
                with open("game_variables/highscore_easy.json", "w") as fp:
                    json.dump(inhalt, fp, indent=2)
                GameVariables.COINS += GameVariables.POINTS
                save_game()
                GameVariables.SAVED = True

            GameScreens.actual_screen = dead_screen(screen, clock, GameVariables.POINTS)
            GameVariables.MISSLE_COUNT = 0
            GameVariables.SAVED = False
        elif GameScreens.actual_screen == GameScreens.INV:
            GameScreens.actual_screen = inventar(screen, clock)
        elif GameScreens.actual_screen == GameScreens.HIGH:
            GameScreens.actual_screen = highscore(screen, clock)
        elif GameScreens.actual_screen == GameScreens.DIFF_P:
            GameScreens.actual_screen = difficulty_play(screen, clock)
        elif GameScreens.actual_screen == GameScreens.DIFF_H:
            GameScreens.actual_screen = difficulty_high(screen, clock)
        elif GameScreens.actual_screen == GameScreens.SHOP:
            GameScreens.actual_screen = shop(screen, clock)

    pygame.quit()



if __name__ == "__main__":
    main()
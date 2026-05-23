import  pygame
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens
from game_variables.player import Player
from game_variables.raptor_enemy import Raptor

def main_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    titel_text = GameVariables.FONT_BIG.render("Dino-Crusher", True, "limegreen")
    starten_text = GameVariables.FONT_MIDDLE.render("Starten", True, "darkgreen")
    quit_text = GameVariables.FONT_MIDDLE.render("Exit", True, "darkred")
    settings_text = GameVariables.FONT_MIDDLE.render("Settings", True, "Orange")

    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    starten_text_rect = starten_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 250))
    quit_text_rect = quit_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 600))
    settings_text_rect = settings_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 400))
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
                    return GameScreens.PLAY
                if quit_text_rect.collidepoint(event.pos):
                    return GameScreens.EXIT
                if settings_text_rect.collidepoint(event.pos):
                    return GameScreens.SETTINGS



        screen.blit(background, (0, 0))
        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=quit_text, dest=quit_text_rect)
        screen.blit(source=settings_text, dest=settings_text_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()




def play_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    pygame.display.set_caption("Play Screen")
    player = Player(screen)
    raptor = Raptor(screen)
    raptor_rect = pygame.Rect(500, player.y_pos + GameVariables.SQUARE_SIZE - 200, 400, 200)
    background = pygame.image.load("assets/map.png").convert()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                player.shoot(mx, my)
                player.glock.shoot()

        screen.fill("black")
        screen.blit(background, (0, 0))
        dmg = raptor.draw(screen, raptor_rect.x, raptor_rect.y)
        dead = player.update_and_draw(dmg)
        player_rect = pygame.Rect(player.x_pos, player.y_pos, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)
        raptor.update(raptor_rect, player_rect)
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
    if GameVariables.FPS_VISIBLE:
        fps_on = GameVariables.FONT_MIDDLE.render("FPS: ON", True, "green")
    else:
        fps_on = GameVariables.FONT_MIDDLE.render("FPS: OFF", True, "red")
    settings_screen = pygame.image.load(
        "assets/background.png").convert()  # chatgpt für einzeigen von Hintergrund verwendet.

    fps_on_rect = fps_on.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
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

                    if GameVariables.FPS_VISIBLE:
                        fps_on = GameVariables.FONT_MIDDLE.render("FPS: ON", True, "green")
                    else:
                        fps_on = GameVariables.FONT_MIDDLE.render("FPS: OFF", True, "red")

        screen.blit(settings_screen, (0, 0))
        screen.blit(source=fps_on, dest=fps_on_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)

def dead_screen(screen: pygame.Surface, clock: pygame.time.Clock):
    died_text = GameVariables.FONT_BIG.render("You died", True, "darkred")
    points_text = GameVariables.FONT_MIDDLE.render("Points:", True, "darkred")
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

def main():
    GameVariables.init()

    pygame.display.set_caption("Hello ")
    screen = pygame.display.set_mode((GameVariables.SCREEN_WIDTH, GameVariables.SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    main_screen(screen, clock)

    while True:
        if GameScreens.actual_screen == GameScreens.MAIN:
            screen.fill("black")
            GameScreens.actual_screen = main_screen(screen, clock)
        elif GameScreens.actual_screen == GameScreens.PLAY:
            GameScreens.actual_screen = play_screen(screen, clock)
        elif GameScreens.actual_screen == GameScreens.SETTINGS:
            GameScreens.actual_screen = settings(screen, clock)
        elif GameScreens.actual_screen == GameScreens.EXIT:
            break
        elif GameScreens.actual_screen == GameScreens.DEAD:
            GameScreens.actual_screen = dead_screen(screen, clock)

    pygame.quit()



if __name__ == "__main__":
    main()

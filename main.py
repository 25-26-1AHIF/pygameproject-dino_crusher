import  pygame
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens
from game_variables.player import Player
def main_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    titel_text = GameVariables.FONT_BIG.render("Dino-Crusher", True, "limegreen")
    starten_text = GameVariables.FONT_MIDDLE.render(">>Starten<<", True, "darkgreen")
    quit_text = GameVariables.FONT_MIDDLE.render(">>Exit<<", True, "darkred")

    titel_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2, 100))
    starten_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2 + GameVariables.SCREEN_WIDTH // 14, 250))
    quit_text_rect = titel_text.get_rect(center=(GameVariables.SCREEN_WIDTH // 2 + GameVariables.SCREEN_WIDTH // 12, 600))
    background = pygame.image.load("assets/background.png") #chatgpt für einzeigen von Hintergrund verwendet.
    screen.blit(background, (0, 0)) #chatgpt für einzeigen von Hintergrund verwendet.
    running = True

    while running:
        shoot = False

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



        #screen.fill("black")

        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=quit_text, dest=quit_text_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()




def play_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    pygame.display.set_caption("Play Screen")
    player = Player(screen)


    running = True

    while running:
        shoot = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN


        screen.fill("black")
        background = pygame.image.load("assets/map.png")
        screen.blit(background, (0, 0))
        player.update_and_draw()
        pygame.display.flip()

        clock.tick(GameVariables.FPS)

    pygame.quit()



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
        elif GameScreens.actual_screen == GameScreens.EXIT:
            break
    pygame.quit()



if __name__ == "__main__":
    main()

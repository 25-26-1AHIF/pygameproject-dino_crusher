import  pygame
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens
from game_variables.player import Player
from game_variables.raptor_enemy import Raptor

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




        screen.blit(source=titel_text, dest=titel_text_rect)
        screen.blit(source=starten_text, dest=starten_text_rect)
        screen.blit(source=quit_text, dest=quit_text_rect)
        pygame.display.flip()
        clock.tick(GameVariables.FPS)
    pygame.quit()




def play_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    pygame.display.set_caption("Play Screen")
    player = Player(screen)
    raptor = Raptor()
    raptor_rect = pygame.Rect(500, GameVariables.SCREEN_HEIGHT - 1 - 120 - 128, 256, 128)

    running = True
    background = pygame.image.load("assets/map.png")
    while running:
        shoot = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameScreens.MAIN

        screen.fill("black")
        screen.blit(background, (0, 0))
        player.update_and_draw()
        player_rect = pygame.Rect(player.x_pos, player.y_pos, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)
        raptor.update(raptor_rect, player_rect)
        raptor.draw(screen, raptor_rect.x, raptor_rect.y)
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

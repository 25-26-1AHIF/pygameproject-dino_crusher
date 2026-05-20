import pygame
from game_variables.game_variables import GameVariables
from game_variables.sprites import Sprite

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x_pos = GameVariables.SCREEN_WIDTH / 2 - GameVariables.SQUARE_SIZE // 2 - 1
        self.y_pos = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE - 1 - 120
        #self.animation = Sprite(filepath="assets/.png", image_count=6, animation_speed=6, image_rect=pygame.Rect(0, 0, 48, 48))
        #self.animation.load_spritesheet()
        self.frame_counter = 0


    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            self.x_pos -= 5
        if keys_pressed[pygame.K_d]:
            self.x_pos += 5

    def update_and_draw(self):

        self.move()
        pygame.draw.rect(surface=self.screen, rect=(self.x_pos,
                                                             self.y_pos,
                                                               GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE), color="red", width=0)
        #self.animation.draw(self.screen, self.x_pos, self.y_pos, self.frame_counter)
        self.frame_counter += 1



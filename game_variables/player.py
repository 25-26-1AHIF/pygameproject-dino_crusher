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
        self.y_velo = 0
        self.gravity = 0.8
        self.jump_strength = -17
        self.on_ground = True


    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            self.x_pos -= 5
        if keys_pressed[pygame.K_d]:
            self.x_pos += 5
        if keys_pressed[pygame.K_SPACE] and self.on_ground:
            self.y_velo = self.jump_strength
            self.on_ground = False

    def update_and_draw(self):

        self.move()
        self.y_velo += self.gravity
        self.y_pos += self.y_velo
        ground_y = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE - 1 - 120        # chatgpt für schwerkraft verwendet (im init und im update_draw)
        if self.y_pos >= ground_y:
            self.y_pos = ground_y
            self.y_velo = 0
            self.on_ground = True

        pygame.draw.rect(surface=self.screen, rect=(self.x_pos,
                                                             self.y_pos,
                                                               GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE), color="red", width=0)
        #self.animation.draw(self.screen, self.x_pos, self.y_pos, self.frame_counter)
        self.frame_counter += 1



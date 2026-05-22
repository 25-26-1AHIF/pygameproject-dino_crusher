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
    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)


    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            self.x_pos -= 5
        if keys_pressed[pygame.K_d]:
            self.x_pos += 5
        if keys_pressed[pygame.K_SPACE] and self.on_ground and self.y_velo == 0:
            self.y_velo = self.jump_strength
            self.on_ground = False



    def update_and_draw(self):
        player_get_rect = self.get_rect()
        rect_2 = pygame.Rect(319, 460, 100, 40)
        rect_3 = pygame.Rect(525, 368, 100, 10)
        rect_4 = pygame.Rect(650, 303, 115, 10)
        rect_5 = pygame.Rect(805, 308, 40, 10)
        rect_6 = pygame.Rect(892, 349, 100, 10)

        self.move()
        self.y_velo += self.gravity
        self.y_pos += self.y_velo
        ground_y = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE - 1 - 120        # chatgpt für schwerkraft verwendet (im init und im update_draw)
        if self.y_pos >= ground_y:
            self.y_pos = ground_y
            self.y_velo = 0
            self.on_ground = True

        if self.y_pos >= rect_2.y - rect_2.height and self.get_rect().colliderect(rect_2):
            if self.y_velo > 0:
                self.y_pos = rect_2.y - rect_2.height
                self.y_velo = 0
                self.on_ground = True
        if self.y_pos >= rect_3.y - rect_3.height and self.get_rect().colliderect(rect_3):
            if self.y_velo > 0:
                self.y_pos = rect_3.y - rect_3.height
                self.y_velo = 0
                self.on_ground = True
        if self.y_pos >= rect_4.y - rect_4.height and self.get_rect().colliderect(rect_4):
            if self.y_velo > 0:
                self.y_pos = rect_4.y - rect_4.height
                self.y_velo = 0
                self.on_ground = True
        if self.y_pos >= rect_5.y - rect_5.height and self.get_rect().colliderect(rect_5):
            if self.y_velo > 0:
                self.y_pos = rect_5.y - rect_5.height
                self.y_velo = 0
                self.on_ground = True
        if self.y_pos >= rect_6.y - rect_6.height and self.get_rect().colliderect(rect_6):
            if self.y_velo > 0:
                self.y_pos = rect_6.y - rect_6.height
                self.y_velo = 0
                self.on_ground = True


        pygame.draw.rect(surface=self.screen, rect=(self.x_pos,
                                                             self.y_pos,
                                                               GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE), color="red", width=0)
        #self.animation.draw(self.screen, self.x_pos, self.y_pos, self.frame_counter)
        self.frame_counter += 1



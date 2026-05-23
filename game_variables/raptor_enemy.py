import pygame
from game_variables.sprites import Sprite as SpriteSheet


class Raptor:
    def __init__(self):
        self.run_anim = SpriteSheet("assets/raptor_run.png", 6, pygame.Rect(0, 0, 128, 64), 8)
        self.run_anim.load_spritesheet()

        self.is_biting = False
        self.frame_counter = 0
        self.facing_left = False

    SPEED = 3

    def update(self, my_rect, player_rect):
        if my_rect.x + self.SPEED < player_rect.x:
            my_rect.x += self.SPEED
            self.facing_left = False
        elif my_rect.x - self.SPEED > player_rect.x:
            my_rect.x -= self.SPEED
            self.facing_left = True

    def draw(self, screen, x, y):
        frame = self.run_anim.images[(self.frame_counter // self.run_anim.aimation_speed) % self.run_anim.image_count]
        scaled = pygame.transform.scale(frame, (256, 128))
        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)
        screen.blit(scaled, (x, y))
        self.frame_counter += 1

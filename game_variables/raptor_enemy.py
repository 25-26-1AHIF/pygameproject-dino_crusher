import pygame
from game_variables.sprites import Sprite as SpriteSheet


class Raptor:
    def __init__(self):
        self.run_anim = SpriteSheet("assets/raptor_run.png", 6, pygame.Rect(0, 0, 128, 64), 8)
        self.run_anim.load_spritesheet()

        self.is_biting = False
        self.frame_counter = 0

    def update(self, player_rect, my_rect):
        # Angriff wenn Spieler nah genug
        if my_rect.colliderect(player_rect.inflate(80, 0)):
            self.is_biting = True
        else:
            self.is_biting = False

    def draw(self, screen, x, y):
        frame = self.run_anim.images[(self.frame_counter // self.run_anim.aimation_speed) % self.run_anim.image_count]
        scaled = pygame.transform.scale(frame, (256, 128))
        screen.blit(scaled, (x, y))
        self.frame_counter += 1

import pygame
from game_variables.sprites import Sprite

class glock:

    def __init__(self, gun_animation, is_shooting, shoot_frame, ):
        self.gun_anim = Sprite("assets/[SHOOT WITH MUZZLE FLASH] Glock - P80 - Kopie.png",
                               12, pygame.Rect(0, 0, 64, 48), 3)
        self.gun_anim.load_spritesheet()
        self.is_shooting = False
        self.shoot_frame = 0

    def draw(self, ):

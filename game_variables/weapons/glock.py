import pygame
from game_variables.sprites import Sprite

class Glock:

    def __init__(self, pfad):
        #self.gun_anim = Sprite("assets/[SHOOT WITH MUZZLE FLASH] Glock - P80 - Kopie.png",
                               #12, pygame.Rect(0, 0, 64, 48), 3)

        #self.gun_anim = Sprite("assets/glock2.png",
                               #2, pygame.Rect(0, 10, 64, 48), 3)

        #self.gun_anim = Sprite("assets/glock3.png",
                               #2, pygame.Rect(0, 10, 64, 48), 3)

        #self.gun_anim = Sprite("assets/glock4.png",
                               #2, pygame.Rect(0, 10, 64, 48), 3)

        self.gun_anim = Sprite(pfad,
                               2, pygame.Rect(0, 10, 64, 48), 3)
        self.gun_anim.load_spritesheet()
        self.is_shooting = False
        self.shoot_frame = 0

    def shoot(self):
        self.is_shooting = True
        self.shoot_frame = 0

    def draw(self, screen, x, y, facing_left):
        if self.is_shooting:
            frame = self.gun_anim.images[self.shoot_frame]
            self.shoot_frame += 1
            if self.shoot_frame >= self.gun_anim.image_count:
                self.is_shooting = False
                self.shoot_frame = 0
        else:
            frame = self.gun_anim.images[0]
        if facing_left:
            frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (x - 20, y + 10))

        else:
            screen.blit(frame, (x + 10, y + 10))
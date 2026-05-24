import random

import pygame
from game_variables.sprites import Sprite as SpriteSheet
from game_variables.player import Player
from game_variables.game_variables import GameVariables
import time
from game_variables.missle import Missle
from game_variables.missle import Missles


class Raptor:
    def __init__(self, screen):
        self.run_anim = SpriteSheet("assets/raptor_run.png", 6, pygame.Rect(0, 0, 128, 64), 8)
        self.run_anim.load_spritesheet()
        self.bite_anim = SpriteSheet("assets/raptor_bite_transparent.png", 10, pygame.Rect(0, 0, 128, 64), 6)
        self.bite_anim.load_spritesheet()
        self.screen = screen
        self.is_biting_x = False
        self.is_biting_y = False
        self.frame_counter = 0
        self.facing_left = False
        self.speed = 6
        self.BITE_RANGE_X = 80
        self.BITE_RANGE_Y = 40
        self.did_damage = False
        self.hp_dino_ges = 10
        self.player_dmg = 5
        self.counter = 0
        self.hp_dino = self.hp_dino_ges
        self.points_raptor = 0

    def get_rect(self, my_rect):        # chatgpt für !!bessere!! hitboxen verwendet
        hitbox_width = 220
        hitbox_height = 70

        hitbox_x = my_rect.x + 90
        hitbox_y = my_rect.y + 110

        return pygame.Rect(
                hitbox_x,
                hitbox_y,
                hitbox_width,
                hitbox_height
            )


    def update(self, my_rect, player_rect):
        # berechnugnen ki claude
        if my_rect.centerx < player_rect.centerx - 60:
            my_rect.x += self.speed
            self.facing_left = False
            # berechnugnen ki claude
        elif my_rect.centerx > player_rect.centerx + 60:
            my_rect.x -= self.speed
            self.facing_left = True
            # berechnugnen ki claude
        self.is_biting_x = my_rect.centerx - 60 <= player_rect.centerx <= my_rect.centerx + 60
        if player_rect.centery <= my_rect.centery:
            self.is_biting_y = True
        else:
            self.is_biting_y = False

    def respawn(self, my_rect):
        x = random.randint(0, 10)
        if x <= 5:
            my_rect.centerx = random.randint(1100, 1200)
        if x > 5:
            my_rect.centerx = random.randint(-120, -20)
        self.counter += 1
        if self.counter == 10:
            self.speed += 1
        if self.counter == 20:
            self.speed += 1
        if self.counter == 30:
            self.hp_dino_ges += 5
        if self.counter == 40:
            self.speed += 1
            self.hp_dino_ges += 5
        self.points_raptor += 10
        GameVariables.ENEMYS_KILLED += 1
        return self.points_raptor



    def draw(self, screen, x, y, missles: Missles, my_rect):               # für die damage ticks chatgpt verwendet damit es nur True returned und somit damage macht wenn die bite animation im 3 frame ist

        if self.is_biting_x and not self.is_biting_y:

            current_frame = (
                    (self.frame_counter // self.bite_anim.aimation_speed)
                    % self.bite_anim.image_count
            )

            frame = self.bite_anim.images[current_frame]


            if current_frame == 0 and not self.did_damage:
                result = True
                self.did_damage = True
            else:
                result = False

        else:
            current_frame = (
                    (self.frame_counter // self.run_anim.aimation_speed)
                    % self.run_anim.image_count
            )

            frame = self.run_anim.images[current_frame]

            result = False

        scaled = pygame.transform.scale(frame, (400, 200))
        if current_frame != 0:
            self.did_damage = False
#
        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)

        screen.blit(scaled, (x, y))
        raptor_rect = self.get_rect(my_rect)
        for missle in missles.missles:
            rocket_rect = missle.get_rect()
            if raptor_rect.colliderect(rocket_rect):
                missles.missles.remove(missle)
                if self.hp_dino <= 0:
                    self.respawn(my_rect=my_rect)
                    self.hp_dino = self.hp_dino_ges
                    break
                else:
                    if GameVariables.ENEMYS_KILLED <= GameVariables.TOLERANCE:
                        self.hp_dino -= self.player_dmg
                    elif GameVariables.ENEMYS_KILLED > GameVariables.TOLERANCE:
                        self.hp_dino -= self.player_dmg + 5

        self.frame_counter += 1

        return result, self.points_raptor



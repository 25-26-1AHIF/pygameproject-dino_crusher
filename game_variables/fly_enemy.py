import random

import pygame
from game_variables.sprites import Sprite as SpriteSheet
from game_variables.player import Player
from game_variables.game_variables import GameVariables
import time
from game_variables.missle import Missle
from game_variables.missle import Missles


class Fly:
    def __init__(self, screen):
        self.run_anim = SpriteSheet("assets/ptero fly - Kopie.png", 6, pygame.Rect(0, 0, 16, 16), 6)
        self.run_anim.load_spritesheet()
        self.bite_anim = SpriteSheet("assets/ptero atack - Kopie.png", 5, pygame.Rect(0, 0, 16, 16), 5)
        self.bite_anim.load_spritesheet()
        self.screen = screen
        self.is_biting_x = False
        self.is_biting_y = False
        self.frame_counter = 0
        self.facing_left = False
        if GameVariables.DIFFICULTY_P == "easy":
            self.speed = 1
        if GameVariables.DIFFICULTY_P == "middle":
            self.speed = 2
        if GameVariables.DIFFICULTY_P == "hard":
            self.speed = 3
        if GameVariables.DIFFICULTY_P == "impossible":
            self.speed = 4
#
        self.BITE_RANGE_X = 20
        self.BITE_RANGE_Y = 10
        self.did_damage = False
        self.hp_dino_ges = 10
        self.player_dmg = 5
        self.counter = 0
        self.hp_dino = self.hp_dino_ges
        self.points_fly = 0


    def get_rect(self, my_rect):        # chatgpt für !!bessere!! hitboxen verwendet
        hitbox_width = 48
        hitbox_height = 48

        hitbox_x = my_rect.x
        hitbox_y = my_rect.y

        return pygame.Rect(
                hitbox_x,
                hitbox_y,
                hitbox_width,
                hitbox_height
            )


    def update(self, my_rect, player_rect):     # chatgpt für das offset verwendet damit dino über player schwebt
        # berechnugnen ki claude
        if my_rect.centerx < player_rect.centerx - 10:
            my_rect.x += self.speed
            self.facing_left = False
            # berechnugnen ki claude
        elif my_rect.centerx > player_rect.centerx + 10:
            my_rect.x -= self.speed
            self.facing_left = True
            # berechnugnen ki claude
        TARGET_OFFSET = 50

        target_y = player_rect.centery - TARGET_OFFSET

        if my_rect.centery > target_y:
            my_rect.y -= self.speed
        elif my_rect.centery < target_y:
            my_rect.y += self.speed
        if player_rect.centery <= 460 and GameVariables.DIFFICULTY_P == "impossible":
            self.speed = 6
        if player_rect.centery <= 460 and GameVariables.DIFFICULTY_P == "hard":
            self.speed = 4
        if player_rect.centery > 460 and GameVariables.DIFFICULTY_P == "impossible":
            self.speed = 4
        if player_rect.centery > 460 and GameVariables.DIFFICULTY_P == "hard":
            self.speed = 3

            # berechnugnen ki claude
        self.is_biting_x = my_rect.centerx - 10 <= player_rect.centerx <= my_rect.centerx + 10
        self.is_biting_y = my_rect.centery - 10 <= player_rect.centery <= my_rect.centery + 10
        if player_rect.centery <= my_rect.centery:
            self.is_biting_y = True
        else:
            self.is_biting_y = False

    def respawn(self, my_rect):
        x = random.randint(0, 10)
        if x <= 5:
            my_rect.centerx = random.randint(1100, 1200)
        else:
            my_rect.centerx = random.randint(-120, -20)
        my_rect.centery = random.randint(0, 300)

        self.counter += 1
        if self.counter == 10:
            self.speed += 1
        if self.counter == 15:
            self.speed += 1
        if self.counter == 30:
            self.hp_dino_ges += 5
            self.speed += 1
        self.points_fly += 10
        GameVariables.ENEMYS_KILLED += 1



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

        scaled = pygame.transform.scale(frame, (48, 48))
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

        return result, self.points_fly



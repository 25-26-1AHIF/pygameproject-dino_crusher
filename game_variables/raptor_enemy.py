import pygame
from game_variables.sprites import Sprite as SpriteSheet
from game_variables.player import Player
from game_variables.game_variables import GameVariables
import time


class Raptor:
    def __init__(self, screen):
        self.run_anim = SpriteSheet("assets/raptor_run.png", 6, pygame.Rect(0, 0, 128, 64), 8)
        self.run_anim.load_spritesheet()
        self.bite_anim = SpriteSheet("assets/raptor_bite_transparent.png", 10, pygame.Rect(0, 0, 128, 64), 6)
        self.bite_anim.load_spritesheet()
        self.screen = screen
        self.player = Player(screen)
        self.is_biting_x = False
        self.is_biting_y = False
        self.frame_counter = 0
        self.facing_left = False
        self.speed = 3
        self.BITE_RANGE_X = 80
        self.BITE_RANGE_Y = 40
        self.did_damage = False


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

    def draw(self, screen, x, y):               # für die damage ticks chatgpt verwendet damit es nur True returned und somit damage macht wenn die bite animation im 3 frame ist

        if self.is_biting_x and not self.is_biting_y:

            current_frame = (
                    (self.frame_counter // self.bite_anim.aimation_speed)
                    % self.bite_anim.image_count
            )

            frame = self.bite_anim.images[current_frame]


            if current_frame == 2 and not self.did_damage:
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
        if current_frame != 2:
            self.did_damage = False

        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)

        screen.blit(scaled, (x, y))

        self.frame_counter += 1

        return result



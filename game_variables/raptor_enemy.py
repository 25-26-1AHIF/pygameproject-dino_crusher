import pygame
from game_variables.sprites import Sprite as SpriteSheet


class Raptor:
    def __init__(self):
        self.run_anim = SpriteSheet("assets/raptor_run.png", 6, pygame.Rect(0, 0, 128, 64), 8)
        self.run_anim.load_spritesheet()
        self.bite_anim = SpriteSheet("assets/raptor_bite_transparent.png", 10, pygame.Rect(0, 0, 128, 64), 6)
        self.bite_anim.load_spritesheet()

        self.is_biting = False
        self.frame_counter = 0
        self.facing_left = False
        self.speed = 3
        self.BITE_RANGE = 80

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
        self.is_biting = my_rect.centerx - 60 <= player_rect.centerx <= my_rect.centerx + 60

    def draw(self, screen, x, y):
        if self.is_biting:
            # berechnugnen ki claude
            frame = self.bite_anim.images[(self.frame_counter // self.bite_anim.aimation_speed) % self.bite_anim.image_count]
        else:

            frame = self.run_anim.images[(self.frame_counter // self.run_anim.aimation_speed) % self.run_anim.image_count]
        scaled = pygame.transform.scale(frame, (400, 200))
        # berechnugnen ki claude

        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)
        screen.blit(scaled, (x, y))
        self.frame_counter += 1

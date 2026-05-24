import time

import pygame
import math
from game_variables.missle import Missle
from game_variables.missle import Missles
from game_variables.game_variables import GameVariables
from game_variables.game_variables import GameScreens
from game_variables.sprites import Sprite
from game_variables.weapons.glock import Glock
from game_variables.weapons.ak47 import Ak

class Player:
    def __init__(self, screen, pfad):
        self.screen = screen
        self.x_pos = GameVariables.SCREEN_WIDTH / 2 - GameVariables.SQUARE_SIZE // 2 - 1
        self.y_pos = GameVariables.SCREEN_HEIGHT - GameVariables.SQUARE_SIZE - 1 - 120
        #self.animation = Sprite(filepath="assets/.png", image_count=6, animation_speed=6, image_rect=pygame.Rect(0, 0, 48, 48))
        #self.animation.load_spritesheet()
        self.frame_counter = 0
        self.y_velo = 0
        self.gravity = 0.8
        self.jump_strength = -17
        self.missles = Missles(screen)
        # Idle Animation: 4 frames, startet bei Frame 0
        self.idle_anim = Sprite("assets/DinoSprites - doux.png", 4, pygame.Rect(0, 0, 24, 24), 6, start_frame=0)
        self.idle_anim.load_spritesheet()
        self.hp = 200
        self.dino_dmg = 40
        self.dino_dmg_fly = 20

        # Run Animation: 6 frames, startet bei Frame 4
        # Gesamte Animation für player mit hochscalieren auf die richtige größe und das teilen der frames weil das bild alle animationen hatte und wir nicht alle wollten mit Claude gemacht
        self.run_anim = Sprite("assets/DinoSprites - doux.png", 6, pygame.Rect(0, 0, 24, 24), 6, start_frame=4)
        self.run_anim.load_spritesheet()

        self.facing_left = False
        self.on_ground = True
        self.shots_fired = 0
        self.reload_time = 2000
        self.last_reload = 0
        self.reloading = False
        self.glock = Glock(pfad=pfad)
        self.ak = Ak()


    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE)




    def move(self):
        keys_pressed = pygame.key.get_pressed()
        is_running = False

        if keys_pressed[pygame.K_a]:
            self.x_pos -= 5
            self.facing_left = True
            is_running = True
        if keys_pressed[pygame.K_d]:
            self.x_pos += 5
            self.facing_left = False
            is_running = True
        if keys_pressed[pygame.K_SPACE] and self.on_ground and self.y_velo == 0:
            self.y_velo = self.jump_strength
            self.on_ground = False

        if is_running:
            frame = self.run_anim.images[(self.frame_counter // self.run_anim.aimation_speed) % self.run_anim.image_count]
        else:
            frame = self.idle_anim.images[(self.frame_counter // self.idle_anim.aimation_speed) % self.idle_anim.image_count]

        frame = pygame.transform.scale(frame, (48, 48))
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        self.screen.blit(frame, (self.x_pos, self.y_pos))
        if GameVariables.ENEMYS_KILLED <= GameVariables.TOLERANCE:
            self.glock.draw(self.screen, self.x_pos, self.y_pos, self.facing_left)
        elif GameVariables.ENEMYS_KILLED > GameVariables.TOLERANCE:
            self.ak.draw(self.screen, self.x_pos, self.y_pos,self.facing_left)


    def shoot(self, mx, my):
        current_time = pygame.time.get_ticks()

        if self.reloading:
            if current_time - self.last_reload >= self.reload_time:         # chatgpt für die logik beim reloaden verwendet
                self.reloading = False
                self.shots_fired = 0
            else:
                return
        missle_x_pos = self.x_pos + GameVariables.SQUARE_SIZE / 2 - 5
        missle_y_pos = self.y_pos + GameVariables.SQUARE_SIZE / 4


        speed = 10
        self.dx = mx - missle_x_pos
        self.dy = my - missle_y_pos
        distance_distance = self.dx * self.dx + self.dy * self.dy
        distance = math.sqrt(distance_distance)     # chatgpt für square root verwendet (habe vergessen wie man sqrt von etwas berechnet)
        self.dx = self.dx / distance * speed
        self.dy = self.dy / distance * speed
        missle = Missle(xpos=missle_x_pos, ypos=missle_y_pos, screen=self.screen, dx=self.dx, dy=self.dy)


        self.missles.add_rocket(missle)
        self.shots_fired += 1
        if GameVariables.ENEMYS_KILLED <= GameVariables.TOLERANCE:
            if self.shots_fired >= 30:
                self.reloading = True
                self.last_reload = current_time
                GameVariables.MAX_BULLETS = 30
            return self.shots_fired
        elif GameVariables.ENEMYS_KILLED > GameVariables.TOLERANCE:
            if self.shots_fired >= 50:
                self.reloading = True
                self.last_reload = current_time
                GameVariables.MAX_BULLETS = 50
            return self.shots_fired


    def update_and_draw(self, dmg, dmg_fly, dmg_fly2):
        player_get_rect = self.get_rect()
        rect_2 = pygame.Rect(319, 460, 100, 40)
        rect_3 = pygame.Rect(525, 369, 100, 10)
        rect_4 = pygame.Rect(650, 303, 115, 10)
        rect_5 = pygame.Rect(805, 308, 40, 10)
        rect_6 = pygame.Rect(892, 349, 100, 10)

        self.missles.update_and_draw()

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

        if dmg == True:
            self.hp -= self.dino_dmg
        if dmg_fly == True:
            self.hp -= self.dino_dmg_fly
        if dmg_fly2 == True:
            self.hp -= self.dino_dmg_fly

        if self.x_pos < -10:
            self.hp -= 1
        if self.x_pos > 1090:
            self.hp -= 1

        if self.hp <= 0:
            return GameScreens.DEAD


        pygame.draw.rect(surface=self.screen, rect=(50, 50, self.hp, 20), color="green", width=0)
        pygame.draw.rect(surface=self.screen, rect=(50, 50, 200, 20), color="black", width=3)

        #pygame.draw.rect(surface=self.screen, rect=(self.x_pos,
                                                             #self.y_pos,
                                                               #GameVariables.SQUARE_SIZE, GameVariables.SQUARE_SIZE), color="red", width=0)

        self.frame_counter += 1



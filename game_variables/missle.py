import pygame
import time
class Missle:

    def __init__(self, xpos, ypos, dx, dy, screen):
        self.xpos = xpos
        self.ypos = ypos
        self.dx = dx
        self.dy = dy
        self.screen = screen

#


    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.xpos, self.ypos, 32, 32)


    def update_and_draw(self):
        self.xpos += self.dx
        self.ypos += self.dy

        pygame.draw.rect(surface=self.screen, rect=(self.xpos, self.ypos, 10, 10), color="gold", width=0)



class Missles:

    def __init__(self, screen: pygame.Surface):
        self.missles = []
        self.screen = screen


    def add_rocket(self, missle: Missle):
        self.missles.append(missle)

    def update_and_draw(self):
        for missle in self.missles[:]:      # habe manchmal error bekommen weil index nicht existiert deshal hat chatgpt gesagt ich soll for missle in self.missles[:]: machen um kopie zu erstellen
            missle.update_and_draw()

            if missle.ypos <= -32:
                self.missles.remove(missle)

            elif missle.ypos >= 720 + 32:
                self.missles.remove(missle)
            elif missle.xpos <= -32:
                self.missles.remove(missle)

            elif missle.xpos >= 1280 + 32:
                self.missles.remove(missle)

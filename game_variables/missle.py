import pygame

class Missle:

    def __init__(self, xpos, ypos, dx, dy, screen):
        self.xpos = xpos
        self.ypos = ypos
        self.dx = dx
        self.dy = dy
        self.screen = screen



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
        for idx, missle in  enumerate(reversed(self.missles)):
            missle.update_and_draw()

            if missle.ypos <=  0 - 32:
                self.missles.pop(len(self.missles) - idx - 1)
import pygame

class Sprite:
    def __init__(self, filepath: str, image_count: int, image_rect: pygame.Rect, animation_speed: int):
        self.filepath = filepath
        self.image_count = image_count
        self.image_rect = image_rect
        self.images: list[pygame.Surface] = []
        self.aimation_speed = animation_speed

    def load_spritesheet(self):
        sprite_sheet = pygame.image.load(self.filepath).convert_alpha()

        for image_index in range(self.image_count):
            image_surface = pygame.Surface(self.image_rect.size, pygame.SRCALPHA).convert_alpha()
            image_surface.blit(sprite_sheet, dest=(0, 0),
                               area=pygame.Rect(image_index * self.image_rect.width, self.image_rect.y,
                                                self.image_rect.width, self.image_rect.height))
            self.images.append(image_surface)

    def draw(self, screen: pygame.Surface, xpos: float, ypos: float, frame_counter: int):
        screen.blit(self.images[(frame_counter // self.aimation_speed) % self.image_count],
                    dest=(xpos, ypos))
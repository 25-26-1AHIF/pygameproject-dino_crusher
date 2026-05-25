import pygame

class Sprite:
    def __init__(self, filepath: str, image_count: int, image_rect: pygame.Rect, animation_speed: int, start_frame: int = 0): # start_frame hinzugefügt - wir haben einen charakter wo alle animationen in einem spritesheet sind, claude gefragt wie man einen bestimmten bereich laden kann
        self.filepath = filepath
        self.image_count = image_count
        self.image_rect = image_rect
        self.images: list[pygame.Surface] = []
        self.aimation_speed = animation_speed
        self.start_frame = start_frame # claude:  wir haben so ein charackter genommen wo alle animatioen in einer png sind
        # sind ich habe claude gefragt wie ich das machen kann
#
    def load_spritesheet(self):
        sprite_sheet = pygame.image.load(self.filepath).convert_alpha()



        for image_index in range(self.image_count):
            image_surface = pygame.Surface(self.image_rect.size, pygame.SRCALPHA).convert_alpha()
            image_surface.blit(sprite_sheet, dest=(0, 0),
                               area=pygame.Rect((self.start_frame + image_index) * self.image_rect.width, self.image_rect.y, # claude: start_frame * width verschiebt den startpunkt im sheet
                                                self.image_rect.width, self.image_rect.height))
            self.images.append(image_surface)
#
    def draw(self, screen: pygame.Surface, xpos: float, ypos: float, frame_counter: int, scale: int = None):
        frame = self.images[(frame_counter // self.aimation_speed) % self.image_count]
        if scale:
            frame = pygame.transform.scale(frame, (scale, scale))
        screen.blit(frame, dest=(xpos, ypos))
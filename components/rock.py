import pygame

class Rock:
    def __init__(self, x, y, size, rock_img=None):
        self.x = x
        self.y = y
        self.size = size
        self.image = rock_img
        
        # Scale the image based on size
        if self.image:
            scale_factor = self.size / 30  # Assuming 30 is the base size
            new_width = int(self.image.get_width() * scale_factor)
            new_height = int(self.image.get_height() * scale_factor)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def draw(self, surface):
        # Draw the rock image
        # Position is adjusted to place the bottom center of the image at (x, y)
        if self.image:
            surface.blit(self.image, (self.x - self.image.get_width() // 2, 
                                     self.y - self.image.get_height()))

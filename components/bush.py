import pygame

class Bush:
    def __init__(self, x, y, size, is_long_bush=False, short_bush_img=None, long_bush_img=None):
        self.x = x
        self.y = y
        self.size = size
        
        # Store the images
        self.short_bush_img = short_bush_img
        self.long_bush_img = long_bush_img
        
        # Use specified bush type
        self.image = long_bush_img if is_long_bush else short_bush_img
        
        # Scale the image based on size
        if self.image:
            scale_factor = self.size / 35  # Assuming 35 is the base size
            new_width = int(self.image.get_width() * scale_factor)
            new_height = int(self.image.get_height() * scale_factor)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def draw(self, surface):
        # Draw the bush image
        # Position is adjusted to place the bottom center of the image at (x, y)
        if self.image:
            surface.blit(self.image, (self.x - self.image.get_width() // 2, 
                                     self.y - self.image.get_height()))

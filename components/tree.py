import pygame

class Tree:
    def __init__(self, x, y, size, is_long_tree=False, tree_img=None, long_tree_img=None):
        self.x = x
        self.y = y
        self.size = size
        
        # Store the images
        self.tree_img = tree_img
        self.long_tree_img = long_tree_img
        
        # Use specified tree type
        self.image = long_tree_img if is_long_tree else tree_img
        
        # Scale the image based on size
        if self.image:
            scale_factor = self.size / 40  # Assuming 40 is the base size
            new_width = int(self.image.get_width() * scale_factor)
            new_height = int(self.image.get_height() * scale_factor)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def draw(self, surface):
        # Draw the tree image
        # Position is adjusted to place the bottom center of the image at (x, y)
        if self.image:
            surface.blit(self.image, (self.x - self.image.get_width() // 2, 
                                     self.y - self.image.get_height()))

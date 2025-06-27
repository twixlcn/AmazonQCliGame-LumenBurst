import pygame

class LightEffect:
    def __init__(self, radius=150, intensity=200, screen_width=800, screen_height=600):
        self.radius = radius
        self.intensity = intensity
        self.position = (0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.glow_surf = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
        self.create_light_surface()
        
    def create_light_surface(self):
        # Pre-render the light surface for better performance
        center = int(self.radius)
        
        # Create a more intense center
        core_radius = int(self.radius * 0.4)  # Inner bright core
        for r in range(core_radius, 0, -1):
            # Higher alpha for the core area
            alpha = min(255, int(self.intensity * 1.5 * (1 - r / self.radius)))
            pygame.draw.circle(
                self.glow_surf, 
                (255, 255, 255, alpha),
                (center, center), 
                r
            )
        
        # Create the outer glow
        for r in range(int(self.radius), core_radius, -2):
            alpha = min(255, int(self.intensity * (1 - r / self.radius)))
            pygame.draw.circle(
                self.glow_surf, 
                (255, 255, 255, alpha),
                (center, center), 
                r
            )
        
    def update(self, mouse_pos):
        self.position = mouse_pos
        
    def draw(self, surface, background):
        # Create a surface for the light mask
        mask = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 220))  # Darker background (increased from 200 to 220)
        
        # Blit the pre-rendered light surface onto the mask
        mask.blit(self.glow_surf, 
                 (int(self.position[0] - self.radius), int(self.position[1] - self.radius)),
                 special_flags=pygame.BLEND_RGBA_SUB)
            
        # Apply the background and mask to the surface
        surface.blit(background, (0, 0))  # Draw background first
        surface.blit(mask, (0, 0))  # Apply the mask with the light effect

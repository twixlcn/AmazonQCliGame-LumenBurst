import random, math, pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 224)


class Firefly:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(4, 8)  # Increased size range from (2,4) to (4,8)
        self.brightness = random.uniform(0.3, 1.0)
        self.speed = random.uniform(0.5, 1.5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.02, 0.05)
        self.pulse_counter = random.uniform(0, 2 * math.pi)
        # Animation states
        self.appearing = True
        self.disappearing = False
        self.clicked = False
        self.animation_progress = 0.0  # 0.0 to 1.0
        self.animation_speed = 0.03  # Slowed down for more consistent appearance

    def update(self):
        # Update position with slight random movement
        self.angle += random.uniform(-0.1, 0.1)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Wrap around screen edges
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
            
        # Pulsating effect
        self.pulse_counter += self.pulse_speed
        self.brightness = 0.5 + 0.5 * math.sin(self.pulse_counter)
        
        # Handle animations
        if self.appearing:
            self.animation_progress += self.animation_speed
            if self.animation_progress >= 1.0:
                self.animation_progress = 1.0
                self.appearing = False
        elif self.disappearing or self.clicked:
            self.animation_progress -= self.animation_speed
            if self.animation_progress <= 0.0:
                self.animation_progress = 0.0
                return True  # Signal to remove this firefly
        
        return False  # Don't remove this firefly yet

    def start_disappearing(self):
        self.disappearing = True
        self.appearing = False
    
    def check_click(self, mouse_pos):
        # Check if the firefly was clicked
        distance = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
        
        # Only allow clicks on fully appeared fireflies
        if distance <= self.size * 4 and not self.appearing and not self.disappearing and not self.clicked:
            self.clicked = True
            self.disappearing = False
            self.appearing = False
            
            # Calculate score based on size - smaller fireflies are worth more points
            # Size ranges from 4-8 (base) or 5-10 (in game)
            # For base size 4: score = 200, for base size 8: score = 100
            # For game size 5: score = 150, for game size 10: score = 50
            if self.size <= 6:  # Smaller fireflies (higher score)
                score_value = int(250 - (self.size * 25))  # 250 - (4*25) = 150, 250 - (6*25) = 100
            else:  # Larger fireflies (lower score)
                score_value = int(150 - (self.size * 10))  # 150 - (7*10) = 80, 150 - (10*10) = 50
            
            # Ensure score is within desired ranges
            score_value = max(50, min(200, score_value))
            
            return True, score_value
        return False, 0

    def draw(self, surface):
        # Draw the firefly with a glowing effect
        glow_radius = self.size * 4  # Increased multiplier from 3 to 4 for larger glow
        
        # Create a surface for the glow
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        
        # Apply animation effects
        animation_factor = self.animation_progress
        current_size = self.size * animation_factor
        current_brightness = self.brightness * animation_factor
        
        # Draw the glow (multiple circles with decreasing alpha)
        for i in range(4):  # Increased from 3 to 4 layers for more detailed glow
            # Ensure alpha is within valid range (0-255)
            alpha = min(255, max(0, int(100 * current_brightness) // (i + 1)))
            radius = glow_radius * animation_factor - i * 2
            if radius > 0:
                pygame.draw.circle(
                    glow_surf, 
                    (LIGHT_YELLOW[0], LIGHT_YELLOW[1], LIGHT_YELLOW[2], alpha),
                    (glow_radius, glow_radius), 
                    radius
                )
        
        # Draw the firefly core
        # Ensure alpha is within valid range (0-255)
        core_alpha = min(255, max(0, int(255 * current_brightness)))
        pygame.draw.circle(
            glow_surf, 
            (YELLOW[0], YELLOW[1], YELLOW[2], core_alpha),
            (glow_radius, glow_radius), 
            current_size
        )
        
        # Draw click effect if clicked
        if self.clicked:
            # Draw expanding ring
            ring_radius = glow_radius * (2.0 - animation_factor)
            ring_width = max(1, int(3 * animation_factor))
            if ring_radius > 0:
                pygame.draw.circle(
                    glow_surf,
                    (255, 255, 255, int(100 * animation_factor)),
                    (glow_radius, glow_radius),
                    int(ring_radius),
                    ring_width
                )
        
        # Blit the glow surface onto the main surface
        surface.blit(glow_surf, (self.x - glow_radius, self.y - glow_radius))

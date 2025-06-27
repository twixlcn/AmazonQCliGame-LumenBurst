import pygame
import sys
import random
import math
from pygame.locals import *
import Firefly
import music

# Initialize pygame
pygame.init()
# Initialize music
music.initialize()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lumen Burst")

# Game states
MAIN_MENU = 0
GAME_PLAYING = 1
GAME_OVER = 2
GAME_WIN = 3
current_game_state = MAIN_MENU

# Global score tracking
final_score = 0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
LIGHT_YELLOW = (255, 255, 224)

# Font
title_font = pygame.font.SysFont('comicsansms', 64)
button_font = pygame.font.SysFont('comicsansms', 36)

# Load images
tree_img = pygame.image.load('assets/tree.png').convert_alpha()
long_tree_img = pygame.image.load('assets/long_tree.png').convert_alpha()
short_bush_img = pygame.image.load('assets/short_bush.png').convert_alpha()
long_bush_img = pygame.image.load('assets/long_bush.png').convert_alpha()
rock_img = pygame.image.load('assets/rock.png').convert_alpha()
light_bg_img = pygame.image.load('assets/light_bg.png').convert()
dark_bg_img = pygame.image.load('assets/dark_bg.png').convert()

# Scale background images to fit screen
light_bg_img = pygame.transform.scale(light_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
dark_bg_img = pygame.transform.scale(dark_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


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


# Tree class
class Tree:
    def __init__(self, x, y, size, is_long_tree=False):
        self.x = x
        self.y = y
        self.size = size
        # Use specified tree type instead of random
        self.image = long_tree_img if is_long_tree else tree_img
        # Scale the image based on size
        scale_factor = self.size / 40  # Assuming 40 is the base size
        new_width = int(self.image.get_width() * scale_factor)
        new_height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def draw(self, surface):
        # Draw the tree image
        # Position is adjusted to place the bottom center of the image at (x, y)
        surface.blit(self.image, (self.x - self.image.get_width() // 2, 
                                 self.y - self.image.get_height()))

# Bush class
class Bush:
    def __init__(self, x, y, size, is_long_bush=False):
        self.x = x
        self.y = y
        self.size = size

        # Use specified bush type instead of random
        self.image = long_bush_img if is_long_bush else short_bush_img
        # Scale the image based on size
        scale_factor = self.size / 35  # Assuming 35 is the base size
        new_width = int(self.image.get_width() * scale_factor)
        new_height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def draw(self, surface):
        # Draw the bush image
        # Position is adjusted to place the bottom center of the image at (x, y)
        surface.blit(self.image, (self.x - self.image.get_width() // 2, 
                                 self.y - self.image.get_height()))

# Rock class
class Rock:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = rock_img
        # Scale the image based on size
        scale_factor = self.size / 30  # Assuming 30 is the base size
        new_width = int(self.image.get_width() * scale_factor)
        new_height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
    def draw(self, surface):
        # Draw the rock image
        # Position is adjusted to place the bottom center of the image at (x, y)
        surface.blit(self.image, (self.x - self.image.get_width() // 2, 
                                 self.y - self.image.get_height()))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=15)
        
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Light effect class
class LightEffect:
    def __init__(self, radius=150, intensity=200):
        self.radius = radius
        self.intensity = intensity
        self.position = (0, 0)
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
        mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 220))  # Darker background (increased from 200 to 220)
        
        # Blit the pre-rendered light surface onto the mask
        mask.blit(self.glow_surf, 
                 (int(self.position[0] - self.radius), int(self.position[1] - self.radius)),
                 special_flags=pygame.BLEND_RGBA_SUB)
            
        # Apply the background and mask to the surface
        surface.blit(background, (0, 0))  # Draw background first
        surface.blit(mask, (0, 0))  # Apply the mask with the light effect

# Create game objects
fireflies = [Firefly() for _ in range(50)]

# Create trees with fixed types (alternating between regular and long trees)
trees = [
    Tree(100, SCREEN_HEIGHT, 30, False),  # Regular tree
    Tree(200, SCREEN_HEIGHT, 25, False),  # Regular tree
    Tree(300, SCREEN_HEIGHT, 20, True),   # Long tree
    Tree(450, SCREEN_HEIGHT, 35, False),  # Regular tree
    Tree(700, SCREEN_HEIGHT, 25, True),   # Long tree
    Tree(600, SCREEN_HEIGHT, 30, True)    # Long tree
]

# Create bushes with fixed types (alternating between short and long bushes)
bushes = [
    Bush(50, SCREEN_HEIGHT, 20, False),  # Short bush
    Bush(150, SCREEN_HEIGHT, 20, True),  # Long bush
    Bush(250, SCREEN_HEIGHT, 25, False),   # Short bush
    Bush(400, SCREEN_HEIGHT, 25, True),   # Long bush
    Bush(550, SCREEN_HEIGHT, 20, False),   # Short bush      
    Bush(650, SCREEN_HEIGHT, 20, True),  # Long bush
    Bush(750, SCREEN_HEIGHT, 20, False),   # Short bush      
]

# Add rocks to the scene
rocks = [
    Rock(180, SCREEN_HEIGHT, 25),
    Rock(450, SCREEN_HEIGHT, 30),
    Rock(620, SCREEN_HEIGHT, 20),
    Rock(350, SCREEN_HEIGHT, 15)
]

# Create play button
play_button = Button(
    SCREEN_WIDTH // 2 - 100,
    SCREEN_HEIGHT // 2 + 50,
    200, 60,
    "PLAY",
    DARK_GREEN,
    GREEN
)

# Game loop
def game_loop():
    music.play_music("bg_music", loops=-1, fade_ms=1000)
    global current_game_state, final_score
    clock = pygame.time.Clock()
    
    # Create a light effect with a smaller radius and higher intensity for a brighter, focused light
    light_effect = LightEffect(radius=100, intensity=400)
    
    # Choose which background to use (dark_bg for this implementation)
    background = dark_bg_img
    
    # Create a list to store fireflies
    game_fireflies = []
    
    # Font for instructions
    instruction_font = pygame.font.SysFont('arial', 16)
    
    # Game speed parameters - defined by score thresholds
    score_thresholds = [0, 1500, 3000, 4500, 7000, 10000]
    difficulty_levels = [0.0, 0.10, 0.25, 0.5, 0.75, 1.0]  # 0.0 to 1.0 scale
    
    # Timing parameters at different difficulty levels
    firefly_lifetime_range = (4000, 2000)  # (slowest, fastest) in milliseconds
    spawn_delay_range = (800, 300)  # (slowest, fastest) in milliseconds
    
    # Current timing values (will change as score increases)
    current_difficulty = 0.0
    firefly_lifetime = firefly_lifetime_range[0]
    firefly_spawn_delay = spawn_delay_range[0]
    
    # Track the last time a firefly was spawned
    last_spawn_time = 0
    
    # Score counter
    score = 0
    previous_level = 0
    level_up_effect = None
    score_font = pygame.font.SysFont('arial', 24)
    
    # Light effect growth parameters
    base_light_radius = 100
    max_light_radius = 250  # Increased maximum to allow for score-based growth
    light_growth_per_click = 15
    light_shrink_rate = 0.2  # Amount to decrease per frame
    
    # Light effect minimum size (game over if reached)
    min_light_radius = base_light_radius  # Game over if light shrinks to this size
    
    # Light shrinking parameters
    light_shrink_timer = 0
    light_shrink_interval = 60  # Frames between automatic light shrinking (1 second at 60 FPS)
    auto_light_shrink_amount = 0.5  # Amount to decrease automatically
    
    # Score-based light radius growth
    light_radius_thresholds = [0, 1000, 3000, 5000, 7500, 10000]
    light_radius_bonuses = [0, 10, 20, 30, 40, 50]  # Additional radius at each threshold
    
    # Click effect parameters
    click_effects = []  # List to store active click effects
    
    # Game win parameters
    win_score = 20000  # Score needed to win
    
    # Start the game timer
    start_time = pygame.time.get_ticks()
    
    while current_game_state == GAME_PLAYING:
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        mouse_clicked = False
        
        # Calculate difficulty based on score thresholds
        difficulty_level = 0
        for i, threshold in enumerate(score_thresholds):
            if score >= threshold:
                difficulty_level = i
        
        # Check for level up
        if difficulty_level > previous_level:
            previous_level = difficulty_level
            music.play_sound("level_up")
            # Create level up effect
            level_up_effect = {
                'timer': 120,  # Show for 2 seconds
                'text': f"LEVEL {difficulty_level + 1}!",
                'size': 48,
                'color': (255, 255, 100)
            }
        
        # Get difficulty percentage based on current level
        current_difficulty = difficulty_levels[difficulty_level]
        
        # Calculate light radius bonus based on score
        light_radius_bonus = 0
        for i, threshold in enumerate(light_radius_thresholds):
            if score >= threshold:
                light_radius_bonus = light_radius_bonuses[i]
        
        # Adjust game speed based on current difficulty
        firefly_lifetime = firefly_lifetime_range[0] - (firefly_lifetime_range[0] - firefly_lifetime_range[1]) * current_difficulty
        firefly_spawn_delay = spawn_delay_range[0] - (spawn_delay_range[0] - spawn_delay_range[1]) * current_difficulty
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    current_game_state = MAIN_MENU
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_clicked = True

        
        # Check if we need to add a new firefly
        if len(game_fireflies) < 5 and current_time - last_spawn_time > firefly_spawn_delay:
            # Create a new stationary firefly
            firefly = Firefly()
            
            # Adjust animation speed based on difficulty
            animation_speed = 0.03 + (0.02 * current_difficulty)  # 0.03 to 0.05
            firefly.animation_speed = animation_speed
            
            firefly.speed = 0  # Make it stationary
            
            # Randomize size with a bias toward different sizes
            # 40% chance for smaller fireflies (5-6)
            # 60% chance for larger fireflies (7-10)
            if random.random() < 0.4:
                firefly.size = random.randint(5, 6)  # Smaller, higher-value fireflies
            else:
                firefly.size = random.randint(7, 10)  # Larger, lower-value fireflies
                
            firefly.brightness = random.uniform(0.6, 1.0)  # Increased minimum brightness
            firefly.animation_progress = 0.0  # Start with 0 for appear animation
            # Add the firefly with its creation time
            game_fireflies.append({
                'firefly': firefly,
                'creation_time': current_time,
                'score_text': None  # Will store score text info when clicked
            })
            last_spawn_time = current_time
        
        # Process fireflies
        fireflies_to_remove = []
        for i, firefly_data in enumerate(game_fireflies):
            firefly = firefly_data['firefly']
            
            # Check if firefly should start disappearing due to timeout
            if not firefly.disappearing and not firefly.clicked:
                if current_time - firefly_data['creation_time'] >= firefly_lifetime:
                    firefly.start_disappearing()
            
            # Check for clicks on fireflies
            if mouse_clicked:
                firefly_hit = False
                for i, firefly_data in enumerate(game_fireflies):
                    firefly = firefly_data['firefly']
                    clicked, points = firefly.check_click(mouse_pos)
                    if clicked:
                        firefly_hit = True
                        music.play_sound("collect_fireflies")
                        score += points
                        
                        # Check if player has won
                        if score >= win_score:
                            final_score = score
                            current_game_state = GAME_WIN
                            
                        # Display floating score text
                        game_fireflies[i]['score_text'] = {
                            'value': points,
                            'position': (firefly.x, firefly.y),
                            'timer': 60,  # Show for 60 frames (1 second at 60 FPS)
                            'color': (255, 255, 100) if points >= 100 else (255, 255, 255)
                        }
                        # Increase light radius when firefly is clicked
                        max_radius_with_bonus = max_light_radius + light_radius_bonus
                        light_effect.radius = min(max_radius_with_bonus, light_effect.radius + light_growth_per_click)
                        # Recreate the light surface with new radius
                        light_effect.glow_surf = pygame.Surface((int(light_effect.radius * 2), int(light_effect.radius * 2)), pygame.SRCALPHA)
                        light_effect.create_light_surface()
                        break  # Only process one click at a time
                
                # Add a click effect regardless of whether a firefly was hit
                if not firefly_hit:
                    click_effects.append({
                        'position': mouse_pos,
                        'timer': 15,  # Show for quarter second
                        'radius': 5,  # Small radius
                        'color': (150, 150, 150, 120)  # Gray with transparency
                    })
            
            # Update firefly and check if it should be removed
            if firefly.update():
                fireflies_to_remove.append(i)
        
        # Remove fireflies that have completed their animations
        for i in sorted(fireflies_to_remove, reverse=True):
            game_fireflies.pop(i)
        
        # Gradually decrease light radius back to base size + score bonus
        target_radius = base_light_radius + light_radius_bonus
        if light_effect.radius > target_radius:
            light_effect.radius -= light_shrink_rate
            if abs(light_effect.radius - target_radius) < light_shrink_rate:
                light_effect.radius = target_radius
            # Recreate the light surface with new radius
            light_effect.glow_surf = pygame.Surface((int(light_effect.radius * 2), int(light_effect.radius * 2)), pygame.SRCALPHA)
            light_effect.create_light_surface()
            
        # Automatic light shrinking over time
        light_shrink_timer += 1
        if light_shrink_timer >= light_shrink_interval:
            light_shrink_timer = 0
            light_effect.radius -= auto_light_shrink_amount
            # Recreate the light surface with new radius
            light_effect.glow_surf = pygame.Surface((int(light_effect.radius * 2), int(light_effect.radius * 2)), pygame.SRCALPHA)
            light_effect.create_light_surface()
            
        # Check if light has returned to its original size (game over)
        # We exclude the beginning of the game with a grace period
        if abs(light_effect.radius - base_light_radius) < 0.5 and current_time - start_time > 3000:  # Give 3 seconds grace period
            # Game over - player's light has returned to original size
            final_score = score
            current_game_state = GAME_OVER
            music.stop_music("bg_music")
            music.play_sound("game_over")
            music.play_music("intro", loops=-1, fade_ms=1000)

            return  # Exit the game loop immediately
        
        # Update click effects
        click_effects_to_remove = []
        for i, effect in enumerate(click_effects):
            effect['timer'] -= 1
            effect['radius'] += 0.5  # Expand the effect
            # Fade out the effect
            alpha = int(120 * (effect['timer'] / 15))
            effect['color'] = (150, 150, 150, alpha)
            
            if effect['timer'] <= 0:
                click_effects_to_remove.append(i)
                
        # Remove expired click effects
        for i in sorted(click_effects_to_remove, reverse=True):
            click_effects.pop(i)
        
        # Update light effect position
        light_effect.update(mouse_pos)
        
        # Draw everything
        light_effect.draw(screen, background)
        
        # Draw click effects
        for effect in click_effects:
            pygame.draw.circle(
                screen,
                effect['color'],
                (int(effect['position'][0]), int(effect['position'][1])),
                int(effect['radius']),
                1  # Line width
            )
        
        # Draw fireflies
        for firefly_data in game_fireflies:
            firefly_data['firefly'].draw(screen)
            
            # Draw floating score text if it exists
            if firefly_data.get('score_text'):
                score_info = firefly_data['score_text']
                if score_info['timer'] > 0:
                    # Make text float upward and fade out
                    score_info['position'] = (score_info['position'][0], score_info['position'][1] - 1)
                    alpha = min(255, int(255 * (score_info['timer'] / 60)))
                    
                    # Create the score text
                    score_font = pygame.font.SysFont('arial', 20)
                    score_surf = score_font.render(f"+{score_info['value']}", True, score_info['color'])
                    score_surf.set_alpha(alpha)
                    
                    # Draw the score text
                    screen.blit(score_surf, (score_info['position'][0] - score_surf.get_width() // 2, 
                                            score_info['position'][1] - score_surf.get_height() // 2))
                    
                    # Decrease timer
                    score_info['timer'] -= 1
        
        # Draw instructions
        instruction_text = instruction_font.render("Move mouse to control light - Click fireflies to increase light - Press ESC to return to menu", True, (255, 255, 255))
        screen.blit(instruction_text, (10, 10))
        
        # Draw score with formatting
        score_text = score_font.render(f"Score: {score:,}", True, (255, 255, 100))  # Yellow color for score
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
        
        # Draw difficulty level
        level_number = difficulty_level + 1  # Convert 0-based index to 1-based level number
        
        # Define color based on level
        if level_number == 1:
            level_color = (50, 255, 50)  # Green for level 1
        elif level_number == 2:
            level_color = (150, 255, 50)  # Yellow-green for level 2
        elif level_number == 3:
            level_color = (255, 255, 50)  # Yellow for level 3
        elif level_number == 4:
            level_color = (255, 150, 50)  # Orange for level 4
        else:
            level_color = (255, 50, 50)  # Red for level 5
            
        level_text = score_font.render(f"Level: {level_number}", True, level_color)
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 40))
        
        # Draw light radius bonus if any
        if light_radius_bonus > 0:
            light_bonus_text = instruction_font.render(f"Light bonus: +{light_radius_bonus}", True, (100, 200, 255))
            screen.blit(light_bonus_text, (SCREEN_WIDTH - light_bonus_text.get_width() - 10, 70))
            y_offset = 100  # For next threshold text
        else:
            y_offset = 70  # For next threshold text
        
        # Show next threshold if not at max level
        if difficulty_level < len(score_thresholds) - 1:
            next_threshold = score_thresholds[difficulty_level + 1]
            points_needed = next_threshold - score
            next_level_text = instruction_font.render(f"Next level: {points_needed:,} points", True, (200, 200, 200))
            screen.blit(next_level_text, (SCREEN_WIDTH - next_level_text.get_width() - 10, y_offset))
            
        # Draw level up effect if active
        if level_up_effect:
            level_up_effect['timer'] -= 1
            
            if level_up_effect['timer'] > 0:
                # Calculate size and opacity based on timer
                size_factor = min(1.0, level_up_effect['timer'] / 60)  # Grows in first half
                if level_up_effect['timer'] > 90:
                    size_factor = (120 - level_up_effect['timer']) / 30  # Start small and grow
                
                opacity = 255
                if level_up_effect['timer'] < 30:
                    opacity = int(255 * level_up_effect['timer'] / 30)  # Fade out in last half second
                
                # Create the font with dynamic size
                dynamic_size = int(level_up_effect['size'] * size_factor)
                level_font = pygame.font.SysFont('comicsansms', dynamic_size)
                
                # Create the text surface
                level_surf = level_font.render(level_up_effect['text'], True, level_up_effect['color'])
                level_surf.set_alpha(opacity)
                
                # Draw centered on screen
                level_rect = level_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(level_surf, level_rect)
            else:
                level_up_effect = None
        
        # Check for game state changes
        if current_game_state != GAME_PLAYING:
            return  # Exit the game loop if state has changed
            
        pygame.display.flip()
        clock.tick(60)

# Main menu loop
def main_menu():
    global current_game_state
    clock = pygame.time.Clock()
    
    # Play intro music when entering main menu
    music.play_music("intro", loops=-1, fade_ms=1000)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
        # Update fireflies
        for firefly in fireflies:
            firefly.update()
        
        # Check button hover and click
        play_button.check_hover(mouse_pos)
        if play_button.is_clicked(mouse_pos, mouse_clicked):
            # Play the button sound effect
            music.play_sound("play")
            # Stop intro music and start the game
            music.stop_music("intro", fade_ms=500)

            global current_game_state
            current_game_state = GAME_PLAYING
            return
        
        # Fill with dark blue for night sky
        screen.fill((10, 10, 40))
        
        # Draw trees, bushes, and rocks
        for tree in trees:
            tree.draw(screen)
        for bush in bushes:
            bush.draw(screen)
        for rock in rocks:
            rock.draw(screen)
        
        # Draw fireflies
        for firefly in fireflies:
            firefly.draw(screen)
        
        # Draw title
        title_text = title_font.render("Lumen Burst", True, LIGHT_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        
        # Add glow effect to title
        glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        for i in range(10, 0, -2):
            alpha = 10 + 5 * i
            pygame.draw.rect(
                glow_surf, 
                (LIGHT_YELLOW[0], LIGHT_YELLOW[1], LIGHT_YELLOW[2], alpha),
                (10 - i, 10 - i, title_rect.width + i * 2, title_rect.height + i * 2),
                border_radius=10
            )
        screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)
        
        # Draw play button
        play_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

# Game over screen
def game_over_screen():
    global current_game_state, final_score
    clock = pygame.time.Clock()
    
    # Create fonts
    title_font = pygame.font.SysFont('comicsansms', 72)
    message_font = pygame.font.SysFont('arial', 32)
    score_font = pygame.font.SysFont('arial', 36)
    instruction_font = pygame.font.SysFont('arial', 24)
    
    # Create restart button
    restart_button = Button(
        SCREEN_WIDTH // 2 - 100,
        SCREEN_HEIGHT // 2 + 80,
        200, 60,
        "RETRY",
        DARK_GREEN,
        GREEN
    )
    
    # Create menu button
    menu_button = Button(
        SCREEN_WIDTH // 2 - 100,
        SCREEN_HEIGHT // 2 + 160,
        200, 60,
        "MENU",
        DARK_GREEN,
        GREEN
    )
    
    # Create some fading fireflies for the background
    fading_fireflies = []
    for _ in range(15):
        firefly = Firefly()
        firefly.speed = 0.2  # Very slow movement
        firefly.size = random.randint(2, 4)  # Smaller size
        firefly.brightness = random.uniform(0.1, 0.3)  # Dimmer
        fading_fireflies.append(firefly)
    
    # Animation variables
    animation_counter = 0
    
    while current_game_state == GAME_OVER:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        animation_counter += 1
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
        # Update fading fireflies
        for firefly in fading_fireflies:
            firefly.update()
        
        # Check button hover and click
        restart_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        
        if restart_button.is_clicked(mouse_pos, mouse_clicked):
            music.play_sound("play")
            current_game_state = GAME_PLAYING
            return
        
        if menu_button.is_clicked(mouse_pos, mouse_clicked):
            music.play_sound("play")
            current_game_state = MAIN_MENU
            return
        
        # Draw everything
        screen.fill((5, 5, 20))  # Darker background
        
        # Draw fading fireflies
        for firefly in fading_fireflies:
            firefly.draw(screen)
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Draw title with pulsating effect
        pulse = math.sin(animation_counter * 0.05) * 20 + 235  # Pulsate between 215-255
        title_color = (255, int(pulse), int(pulse))  # Pulsating red
        
        title_text = title_font.render("GAME OVER", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        
        # Add shadow effect to title
        shadow_text = title_font.render("GAME OVER", True, (40, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 - 116))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Draw message
        message_text = message_font.render("You missed the fireflies too many times!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(message_text, message_rect)
        
        # Draw score
        score_text = score_font.render(f"Final Score: {final_score:,}", True, (255, 255, 100))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(score_text, score_rect)
        
        # Draw buttons
        restart_button.draw(screen)
        menu_button.draw(screen)
        
        # Draw tip
        tip_text = instruction_font.render("Tip: Click carefully when you see a firefly!", True, (200, 200, 200))
        tip_rect = tip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(tip_text, tip_rect)
        
        pygame.display.flip()
        clock.tick(60)

# Win screen
def win_screen():
    global current_game_state, final_score
    clock = pygame.time.Clock()
    
    # Create fonts
    title_font = pygame.font.SysFont('comicsansms', 64)
    message_font = pygame.font.SysFont('arial', 32)
    instruction_font = pygame.font.SysFont('arial', 24)
    
    # Create restart button
    restart_button = Button(
        SCREEN_WIDTH // 2 - 145,
        SCREEN_HEIGHT // 2 + 50,
        300, 60,
        "PLAY AGAIN",
        DARK_GREEN,
        GREEN
    )
    
    # Create menu button
    menu_button = Button(
        SCREEN_WIDTH // 2 - 100,
        SCREEN_HEIGHT // 2 + 130,
        200, 60,
        "MENU",
        DARK_GREEN,
        GREEN
    )
    
    # Create victory fireflies
    victory_fireflies = [Firefly() for _ in range(100)]
    for firefly in victory_fireflies:
        firefly.size = random.randint(3, 8)
        firefly.brightness = random.uniform(0.7, 1.0)
    
    while current_game_state == GAME_WIN:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
        # Update fireflies
        for firefly in victory_fireflies:
            firefly.update()
        
        # Check button hover and click
        restart_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        
        if restart_button.is_clicked(mouse_pos, mouse_clicked):
            current_game_state = GAME_PLAYING
            return
        
        if menu_button.is_clicked(mouse_pos, mouse_clicked):
            current_game_state = MAIN_MENU
            return
        
        # Draw everything
        screen.fill((10, 10, 40))  # Dark blue background
        
        # Draw fireflies
        for firefly in victory_fireflies:
            firefly.draw(screen)
        
        # Draw title with glow effect
        title_text = title_font.render("YOU WIN!", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        
        # Add glow effect to title
        glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        for i in range(10, 0, -2):
            alpha = 10 + 5 * i
            pygame.draw.rect(
                glow_surf, 
                (255, 255, 100, alpha),
                (10 - i, 10 - i, title_rect.width + i * 2, title_rect.height + i * 2),
                border_radius=10
            )
        screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)
        
        # Draw message
        message_text = message_font.render(f"You collected {final_score:,} points!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(message_text, message_rect)
        
        # Draw buttons
        restart_button.draw(screen)
        menu_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    while True:
        if current_game_state == MAIN_MENU:
            main_menu()
        elif current_game_state == GAME_PLAYING:
            game_loop()
        elif current_game_state == GAME_OVER:
            game_over_screen()
        elif current_game_state == GAME_WIN:
            win_screen()
import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

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

# Firefly class
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
        self.animation_speed = 0.05

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
        if distance <= self.size * 4:  # Increased click area from 3 to 4 times the size
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
    global current_game_state
    clock = pygame.time.Clock()
    
    # Create a light effect with a smaller radius and higher intensity for a brighter, focused light
    light_effect = LightEffect(radius=100, intensity=400)  # Increased intensity from 300 to 400
    
    # Choose which background to use (dark_bg for this implementation)
    background = dark_bg_img
    
    # Create a list to store fireflies
    game_fireflies = []
    
    # Font for instructions
    instruction_font = pygame.font.SysFont('arial', 16)
    
    # Time (in milliseconds) each firefly should stay visible
    firefly_lifetime = 3000  # 3 seconds
    
    # Time (in milliseconds) between new firefly appearances
    firefly_spawn_delay = 500  # 0.5 seconds
    
    # Track the last time a firefly was spawned
    last_spawn_time = 0
    
    # Score counter
    score = 0
    score_font = pygame.font.SysFont('arial', 24)
    
    # Light effect growth parameters
    base_light_radius = 100
    max_light_radius = 200
    light_growth_per_click = 15
    light_shrink_rate = 0.2  # Amount to decrease per frame
    
    # Miss effect parameters
    miss_effects = []  # List to store active miss effects
    
    # Game win/lose parameters
    misses_allowed = 10  # Number of misses before game over
    current_misses = 0
    win_score = 100000  # Score needed to win
    
    # Start the game timer
    start_time = pygame.time.get_ticks()
    
    while current_game_state == GAME_PLAYING:
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        mouse_clicked = False
        
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
            if not firefly.disappearing and not firefly.clicked and current_time - firefly_data['creation_time'] >= firefly_lifetime:
                firefly.start_disappearing()
            
            # Check for clicks on fireflies
            if mouse_clicked:
                firefly_hit = False
                for i, firefly_data in enumerate(game_fireflies):
                    firefly = firefly_data['firefly']
                    clicked, points = firefly.check_click(mouse_pos)
                    if clicked:
                        firefly_hit = True
                        score += points
                        
                        # Check if player has won
                        if score >= win_score:
                            current_game_state = GAME_WIN
                            
                        # Display floating score text
                        game_fireflies[i]['score_text'] = {
                            'value': points,
                            'position': (firefly.x, firefly.y),
                            'timer': 60,  # Show for 60 frames (1 second at 60 FPS)
                            'color': (255, 255, 100) if points >= 100 else (255, 255, 255)
                        }
                        # Increase light radius when firefly is clicked
                        light_effect.radius = min(max_light_radius, light_effect.radius + light_growth_per_click)
                        # Recreate the light surface with new radius
                        light_effect.glow_surf = pygame.Surface((int(light_effect.radius * 2), int(light_effect.radius * 2)), pygame.SRCALPHA)
                        light_effect.create_light_surface()
                        break  # Only process one click at a time
                
                # If no firefly was hit, check if we clicked near any firefly
                if not firefly_hit:
                    near_firefly = False
                    for firefly_data in game_fireflies:
                        firefly = firefly_data['firefly']
                        # Calculate distance to firefly
                        distance = math.sqrt((mouse_pos[0] - firefly.x)**2 + (mouse_pos[1] - firefly.y)**2)
                        # Check if click was near a firefly (within a reasonable distance)
                        if distance <= firefly.size * 8:  # Wider area to detect "near misses"
                            near_firefly = True
                            break
                    
                    # Only count as a miss if we were trying to click a firefly but missed
                    if near_firefly:
                        miss_effects.append({
                            'position': mouse_pos,
                            'timer': 30,  # Show for half a second
                            'radius': 10,  # Starting radius
                            'color': (255, 50, 50, 180)  # Red with some transparency
                        })
                        current_misses += 1
                        
                        # Check if player has lost
                        if current_misses >= misses_allowed:
                            current_game_state = GAME_OVER
                    else:
                        # Just a background click, show a subtle effect but don't count as miss
                        miss_effects.append({
                            'position': mouse_pos,
                            'timer': 15,  # Show for quarter second (shorter)
                            'radius': 5,  # Smaller radius
                            'color': (150, 150, 150, 120)  # Gray with more transparency
                        })
            
            # Update firefly and check if it should be removed
            if firefly.update():
                fireflies_to_remove.append(i)
        
        # Remove fireflies that have completed their animations
        for i in sorted(fireflies_to_remove, reverse=True):
            game_fireflies.pop(i)
        
        # Gradually decrease light radius back to base size
        if light_effect.radius > base_light_radius:
            light_effect.radius -= light_shrink_rate
            if abs(light_effect.radius - base_light_radius) < light_shrink_rate:
                light_effect.radius = base_light_radius
            # Recreate the light surface with new radius
            light_effect.glow_surf = pygame.Surface((int(light_effect.radius * 2), int(light_effect.radius * 2)), pygame.SRCALPHA)
            light_effect.create_light_surface()
        
        # Update miss effects
        miss_effects_to_remove = []
        for i, effect in enumerate(miss_effects):
            effect['timer'] -= 1
            effect['radius'] += 0.8  # Expand the effect
            # Fade out the effect
            alpha = int(180 * (effect['timer'] / 30))
            effect['color'] = (255, 50, 50, alpha)
            
            if effect['timer'] <= 0:
                miss_effects_to_remove.append(i)
                
        # Remove expired miss effects
        for i in sorted(miss_effects_to_remove, reverse=True):
            miss_effects.pop(i)
        
        # Update light effect position
        light_effect.update(mouse_pos)
        
        # Draw everything
        light_effect.draw(screen, background)
        
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
        
        # Draw misses remaining
        misses_remaining = misses_allowed - current_misses
        misses_color = (255, 255, 255)  # White by default
        if misses_remaining <= 3:
            misses_color = (255, 50, 50)  # Red when low on misses
        misses_text = score_font.render(f"Misses: {current_misses}/{misses_allowed}", True, misses_color)
        screen.blit(misses_text, (SCREEN_WIDTH - misses_text.get_width() - 10, 40))
        
        # Check for game state changes
        if current_game_state != GAME_PLAYING:
            return  # Exit the game loop if state has changed
            
        pygame.display.flip()
        clock.tick(60)

# Main menu loop
def main_menu():
    global current_game_state
    clock = pygame.time.Clock()
    
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
            # Start the game
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
# Game over screen
def game_over_screen():
    global current_game_state
    clock = pygame.time.Clock()
    
    # Create fonts
    title_font = pygame.font.SysFont('comicsansms', 64)
    message_font = pygame.font.SysFont('arial', 32)
    instruction_font = pygame.font.SysFont('arial', 24)
    
    # Create restart button
    restart_button = Button(
        SCREEN_WIDTH // 2 - 100,
        SCREEN_HEIGHT // 2 + 50,
        200, 60,
        "RESTART",
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
    
    while current_game_state == GAME_OVER:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
        
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
        
        # Draw title
        title_text = title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # Draw message
        message_text = message_font.render("You missed the fireflies too many times!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(message_text, message_rect)
        
        # Draw buttons
        restart_button.draw(screen)
        menu_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

# Win screen
def win_screen():
    global current_game_state
    clock = pygame.time.Clock()
    
    # Create fonts
    title_font = pygame.font.SysFont('comicsansms', 64)
    message_font = pygame.font.SysFont('arial', 32)
    instruction_font = pygame.font.SysFont('arial', 24)
    
    # Create restart button
    restart_button = Button(
        SCREEN_WIDTH // 2 - 100,
        SCREEN_HEIGHT // 2 + 50,
        200, 60,
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
        message_text = message_font.render("You collected 100,000 points!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(message_text, message_rect)
        
        # Draw buttons
        restart_button.draw(screen)
        menu_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

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

# Firefly class
class Firefly:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(2, 4)
        self.brightness = random.uniform(0.3, 1.0)
        self.speed = random.uniform(0.5, 1.5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.02, 0.05)
        self.pulse_counter = random.uniform(0, 2 * math.pi)

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

    def draw(self, surface):
        # Draw the firefly with a glowing effect
        glow_radius = self.size * 3
        
        # Create a surface for the glow
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        
        # Draw the glow (multiple circles with decreasing alpha)
        for i in range(3):
            alpha = int(100 * self.brightness) // (i + 1)
            radius = glow_radius - i * 2
            if radius > 0:
                pygame.draw.circle(
                    glow_surf, 
                    (LIGHT_YELLOW[0], LIGHT_YELLOW[1], LIGHT_YELLOW[2], alpha),
                    (glow_radius, glow_radius), 
                    radius
                )
        
        # Draw the firefly core
        pygame.draw.circle(
            glow_surf, 
            (YELLOW[0], YELLOW[1], YELLOW[2], int(255 * self.brightness)),
            (glow_radius, glow_radius), 
            self.size
        )
        
        # Blit the glow surface onto the main surface
        surface.blit(glow_surf, (self.x - glow_radius, self.y - glow_radius))

# Tree class
class Tree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        # Randomly choose between regular and long tree
        self.image = tree_img if random.random() > 0.5 else long_tree_img
        
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
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        # Randomly choose between short and long bush
        self.image = short_bush_img if random.random() > 0.5 else long_bush_img
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

# Create game objects
fireflies = [Firefly() for _ in range(50)]
trees = [
    Tree(100, SCREEN_HEIGHT, 30),
    Tree(300, SCREEN_HEIGHT, 20),
    Tree(500, SCREEN_HEIGHT, 35),
    Tree(700, SCREEN_HEIGHT, 25),
    Tree(200, SCREEN_HEIGHT, 25),
    Tree(600, SCREEN_HEIGHT, 30)
]

bushes = [
    Bush(150, SCREEN_HEIGHT - 30, 20),
    Bush(400, SCREEN_HEIGHT - 25, 25),
    Bush(650, SCREEN_HEIGHT - 35, 20),
    Bush(250, SCREEN_HEIGHT - 20, 25),
    Bush(550, SCREEN_HEIGHT - 30, 20)
]

# Add rocks to the scene
rocks = [
    Rock(180, SCREEN_HEIGHT - 15, 25),
    Rock(450, SCREEN_HEIGHT - 20, 30),
    Rock(620, SCREEN_HEIGHT - 15, 20),
    Rock(350, SCREEN_HEIGHT - 10, 15)
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

# Main game loop
def main_menu():
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
            # This would start the game
            print("Starting the game!")
            # For now, we'll just continue showing the menu
        
        # Draw everything
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
    main_menu()

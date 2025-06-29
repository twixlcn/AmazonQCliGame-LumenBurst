import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Dictionaries to store loaded music and sound effects
music_tracks = {}
sound_effects = {}

def load_music(name, file_path):
    """
    Load a music file and store it in the music_tracks dictionary
    
    Args:
        name (str): The name to reference the music by
        file_path (str): Path to the music file
    """
    if os.path.exists(file_path):
        music_tracks[name] = file_path
    else:
        print(f"Warning: Music file not found: {file_path}")

def load_sound(name, file_path):
    """
    Load a sound effect and store it in the sound_effects dictionary
    
    Args:
        name (str): The name to reference the sound by
        file_path (str): Path to the sound file
    """
    if os.path.exists(file_path):
        sound_effects[name] = pygame.mixer.Sound(file_path)
    else:
        print(f"Warning: Sound file not found: {file_path}")

def play_music(name, loops=-1, fade_ms=0):
    """
    Play a music track
    
    Args:
        name (str): The name of the music to play
        loops (int): Number of times to repeat (-1 for infinite)
        fade_ms (int): Fade-in time in milliseconds
    """
    if name in music_tracks:
        pygame.mixer.music.load(music_tracks[name])
        pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
    else:
        print(f"Warning: Music '{name}' not loaded")

def play_sound(name, volume=0.2):
    """
    Play a sound effect
    
    Args:
        name (str): The name of the sound to play
        volume (float): Volume level from 0.0 to 1.0
    """
    if name in sound_effects:
        sound_effects[name].set_volume(volume)
        sound_effects[name].play()
    else:
        print(f"Warning: Sound '{name}' not loaded")

def stop_music(name, fade_ms=0):
    """
    Stop the currently playing music
    
    Args:
        fade_ms (int): Fade-out time in milliseconds
    """
    pygame.mixer.music.fadeout(fade_ms)

def set_volume(volume):
    """
    Set the music volume
    
    Args:
        volume (float): Volume level from 0.0 to 1.0
    """
    pygame.mixer.music.set_volume(volume)

# Load all music files at startup
def initialize():
    """Initialize and load all music files and sound effects"""
    
    # Load background music
    load_music("intro", "assets/music/intro.mp3")
    load_music("bg_music", "assets/music/bg_music.mp3")
    
    # Load sound effects
    load_sound("collect_fireflies", "assets/music/collect_fireflies.mp3")
    load_sound("level_up", "assets/music/level_up.wav")
    load_sound("play", "assets/music/play.wav")
    load_sound("game_over", "assets/music/game_over.wav")

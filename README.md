# Lumen Burst

## Game Concept

Lumen Burst is an enchanting, atmospheric game where players control a magical light in a dark forest filled with fireflies. As the keeper of the light, your goal is to maintain and grow your luminescence by capturing the fleeting glow of fireflies before they disappear into the night.

The game combines quick reflexes, strategic timing, and resource management as you navigate through increasingly difficult levels. Your light constantly dims over time, and only by capturing fireflies can you sustain and expand your radiance. However, as you progress through levels, the game becomes more challenging - fireflies move faster, disappear quicker, and you're allowed fewer misses.

## Game Mechanics

### Light Mechanics
- You control a circular light that follows your mouse cursor
- Your light constantly shrinks over time
- If your light shrinks to its minimum size, the game ends
- Clicking on fireflies increases your light's radius
- The maximum light radius increases as you earn more points

### Firefly Mechanics
- Fireflies appear randomly across the screen
- Each firefly has a limited lifespan before it fades away
- Smaller fireflies are worth more points (50-200 points)
- Clicking on a firefly captures its light energy and increases your score
- Missing a firefly (letting it disappear) counts against your missed firefly limit

### Level Progression
- The game has 5 difficulty levels
- You advance levels by reaching score thresholds:
  - Level 1: 0-1,499 points
  - Level 2: 1,500-2,999 points
  - Level 3: 3,000-4,499 points
  - Level 4: 4,500-6,999 points
  - Level 5: 7,000+ points
- Each level increases the game's difficulty:
  - Fireflies have shorter lifespans
  - Fireflies spawn more frequently
  - The allowed number of missed fireflies decreases

### Missed Firefly Limits
- Level 1: Unlimited misses allowed
- Level 2: Maximum 15 missed fireflies
- Level 3: Maximum 10 missed fireflies
- Level 4: Maximum 5 missed fireflies
- Level 5: No missed fireflies allowed (0)

### Winning and Losing
- **Win Condition**: Reach 20,000 points
- **Lose Conditions**:
  1. Your light shrinks to its minimum size
  2. You exceed the missed firefly limit for your current level

## Controls
- **Mouse Movement**: Control the position of your light
- **Left Click**: Capture fireflies
- **ESC**: Return to the main menu

## Visual Elements
- A dark forest background with trees, bushes, and rocks
- A player-controlled light that illuminates the surroundings
- Animated fireflies that pulse with light
- Visual effects when capturing fireflies
- Level-up notifications
- Score and level indicators

## Audio Elements
- Background music that sets the atmosphere
- Sound effects for:
  - Capturing fireflies
  - Leveling up
  - Game over
  - Menu interactions

## Tips for Success
1. Focus on smaller fireflies as they're worth more points
2. Be strategic about which fireflies to pursue - don't chase ones that are about to disappear
3. In higher levels, prioritize not missing fireflies over maximizing points
4. Keep an eye on your missed firefly counter in levels 2+
5. Try to maintain a balance between growing your light and advancing to higher levels

## Technical Requirements
- Python 3.x
- Pygame library

Enjoy the magical world of Lumen Burst, where your skill at capturing the ephemeral light of fireflies determines how brightly you'll shine in the darkness!

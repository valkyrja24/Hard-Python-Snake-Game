# 🐍 Snake Game

A modern, feature-rich implementation of the classic Snake game built with Python and Tkinter. Supports both single-player and two-player modes with smooth animations and visual effects.

## Features

- **Single Player & Two Player Modes**
- **Smooth Gameplay** with progressive speed increase
- **Pause Functionality** (Press P)
- **Visual Enhancements**:
  - Animated snake eyes that follow direction
  - Pulsing food with glow effect
  - Subtle grid background
  - 3-2-1 countdown before game start
  - Speed indicator
- **Winner Detection** in two-player mode
- **Clean UI** with game over screen and controls display

## Requirements

- Python 3.6+
- Tkinter (usually included with Python)

## Installation

1. Clone or download all game files to a directory
2. Ensure you have the following files:
   - `main.py`
   - `game_manager.py`
   - `game.py`
   - `menu.py`
   - `snake.py`
   - `food.py`
   - `settings.py`

## How to Run

```bash
python main.py
```

## Controls

### Menu
- **1** - Start Single Player Game
- **2** - Start Two Player Game
- **Q** - Quit Game

### In Game

#### Player 1
- **Arrow Keys** - Move snake (Up/Down/Left/Right)

#### Player 2 (Two Player Mode)
- **W** - Move Up
- **A** - Move Left
- **S** - Move Down
- **D** - Move Right

#### Game Controls
- **P** - Pause/Unpause
- **R** - Restart Game
- **M** - Return to Menu
- **Q** - Quit Game

## Game Rules

1. Control your snake to eat the red food
2. Each food eaten increases your score and snake length
3. Game speed increases gradually as you eat more food
4. Avoid hitting walls, yourself, or the other player (in two-player mode)
5. In two-player mode, the player with the highest score when both die wins

## Configuration

You can customize game settings in `settings.py`:

- `CELL_SIZE` - Size of each grid cell (default: 20)
- `GRID_WIDTH` - Grid width in cells (default: 30)
- `GRID_HEIGHT` - Grid height in cells (default: 20)
- `INITIAL_DELAY` - Starting game speed in ms (default: 150)
- `MIN_DELAY` - Fastest possible speed in ms (default: 50)
- `SPEEDUP_FACTOR` - Speed multiplier per food (default: 0.98)
- Color scheme settings

## Game Architecture

- **game_manager.py** - Manages game state transitions and window lifecycle
- **game.py** - Main game logic and rendering
- **menu.py** - Main menu interface
- **snake.py** - Snake entity with movement and collision
- **food.py** - Food spawning and positioning
- **settings.py** - Global configuration and constants

## Tips

- Start slow and plan your path ahead
- In two-player mode, you can trap your opponent by cutting off their path
- Watch the speed indicator - the game gets progressively faster
- Use pause (P) to take a break or plan your next move

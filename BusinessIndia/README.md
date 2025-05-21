# Business India: The Board Game

A digital version of the classic Business India board game implemented in Python using Pygame.

## Features

- 2D game board with Indian cities as properties
- Support for 2-4 players
- Dice rolling mechanics
- Property buying and rent collection
- Chance cards with random events
- Player tokens and movement
- Financial transactions
- Game state management

## How to Play

1. Run the game: `python main.py`
2. The game starts with 4 players (can be modified in the code)
3. Players take turns rolling the dice and moving around the board
4. Land on properties to buy them or pay rent
5. Manage your money wisely to avoid bankruptcy
6. The last player standing wins!

## Game Controls

- **Roll Dice Button**: Roll the dice and move your token
- **End Turn Button**: End your turn after completing actions
- **Buy Property Button**: Purchase the property you landed on (if available)

## Game Elements

- **Properties**: Various Indian states with different prices and rent values
- **Chance Cards**: Random events that can help or hinder your progress
- **GO**: Collect ₹200 when you pass or land on GO
- **Jail**: Just visiting or sent to jail
- **Free Parking**: Take a break!

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py`

## Project Structure

- `main.py`: Main game loop and initialization
- `board.py`: Board representation and rendering
- `player.py`: Player class with movement and financial logic
- `property.py`: Property class with ownership and rent calculation
- `game.py`: Game state management and rules
- `ui.py`: User interface elements (buttons, panels, etc.)

## Future Improvements

- Add sound effects and music
- Implement property upgrades (houses and hotels)
- Add multiplayer networking support
- Create a game setup screen for player customization
- Add AI players
- Implement save/load game functionality

import pygame
import sys
import random
from pygame.locals import *
from board import Board
from player import Player
from game import BusinessIndiaGame
from ui import Button, PlayerPanel, PropertyInfoPanel, DicePanel, MessagePanel

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FONT_SIZE = 24

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Business India: The Board Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

def setup_game():
    game = BusinessIndiaGame()
    
    # Add players with different colors
    game.add_player("Player 1", RED)
    game.add_player("Player 2", BLUE)
    game.add_player("Player 3", GREEN)
    game.add_player("Player 4", YELLOW)
    
    game.game_state = "playing"
    return game

def main():
    # Create game objects
    game = setup_game()
    board = Board(600, 600)
    
    # Create UI elements
    player_panel = PlayerPanel(750, 100, 250, 300)
    property_panel = PropertyInfoPanel(750, 420, 250, 200)
    dice_panel = DicePanel(750, 640, 250, 120)
    message_panel = MessagePanel(100, 720, 600, 100)
    
    # Create buttons
    roll_button = Button(20, 720, 100, 30, "Roll Dice", (100, 100, 255), (150, 150, 255))
    end_turn_button = Button(130, 720, 100, 30, "End Turn", (255, 100, 100), (255, 150, 150))
    
    # Game state variables
    dice_rolled = False
    buy_button = None
    
    # Game loop
    running = True
    while running:
        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_clicked = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        # Update game state
        if game.game_state == "playing":
            current_player = game.get_current_player()
            
            # Check button hover states
            roll_button.check_hover(mouse_pos)
            end_turn_button.check_hover(mouse_pos)
            
            # Handle button clicks
            if roll_button.is_clicked(mouse_pos, mouse_clicked) and not dice_rolled:
                # Roll dice
                dice_panel.start_rolling()
                game.dice_value = game.roll_dice()
                current_player.move(game.dice_value)
                dice_rolled = True
                
                # Handle landing on a space
                game.handle_player_landed()
                message_panel.set_message(game.message)
                
                # Update property panel if landed on property
                property = game.get_property_at_position(current_player.position)
                property_panel.set_property(property)
            
            if end_turn_button.is_clicked(mouse_pos, mouse_clicked) and dice_rolled:
                # End turn
                game.next_turn()
                dice_rolled = False
                message_panel.set_message(f"{game.get_current_player().name}'s turn")
            
            # Handle property buying
            if buy_button and buy_button.is_clicked(mouse_pos, mouse_clicked):
                property = game.get_property_at_position(current_player.position)
                if property:
                    game.buy_property(current_player, property)
                    message_panel.set_message(game.message)
        
        # Update dice animation
        dice_panel.update()
        
        # Draw everything
        screen.fill(WHITE)
        
        # Draw board
        board.draw(screen)
        
        # Draw players on board
        for player in game.players:
            player.draw(screen, board)
        
        # Draw UI panels
        player_panel.draw(screen, game.players, game.current_player_index)
        buy_button = property_panel.draw(screen, game.get_current_player())
        dice_panel.draw(screen, game.dice_value)
        message_panel.draw(screen)
        
        # Draw buttons
        roll_button.draw(screen)
        end_turn_button.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

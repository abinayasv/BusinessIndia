import pygame

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spaces = []
        self.initialize_spaces()
        
    def initialize_spaces(self):
        # Define board spaces with their positions
        # Format: (name, type, position, coordinates)
        
        # Board dimensions
        board_size = 600
        board_x = 100
        board_y = 100
        space_size = 60
        
        # Create spaces around the board (40 spaces total)
        # Bottom row (GO to JAIL)
        for i in range(11):
            x = board_x + board_size - (i * space_size)
            y = board_y + board_size
            position = i
            if i == 0:
                space_type = "go"
                name = "GO"
            elif i == 10:
                space_type = "jail"
                name = "JAIL"
            elif i % 2 == 0:
                space_type = "property"
                name = f"Property {i}"
            else:
                space_type = "chance"
                name = "Chance"
            
            self.spaces.append({
                "name": name,
                "type": space_type,
                "position": position,
                "x": x,
                "y": y
            })
        
        # Left column
        for i in range(1, 10):
            x = board_x
            y = board_y + board_size - (i * space_size)
            position = 10 + i
            if i % 2 == 0:
                space_type = "property"
                name = f"Property {position}"
            else:
                space_type = "chance"
                name = "Chance"
            
            self.spaces.append({
                "name": name,
                "type": space_type,
                "position": position,
                "x": x,
                "y": y
            })
        
        # Top row
        for i in range(11):
            x = board_x + (i * space_size)
            y = board_y
            position = 20 + i
            if i == 0:
                space_type = "free_parking"
                name = "FREE PARKING"
            elif i == 10:
                space_type = "go_to_jail"
                name = "GO TO JAIL"
            elif i % 2 == 0:
                space_type = "property"
                name = f"Property {position}"
            else:
                space_type = "chance"
                name = "Chance"
            
            self.spaces.append({
                "name": name,
                "type": space_type,
                "position": position,
                "x": x,
                "y": y
            })
        
        # Right column
        for i in range(1, 10):
            x = board_x + board_size
            y = board_y + (i * space_size)
            position = 30 + i
            if i % 2 == 0:
                space_type = "property"
                name = f"Property {position}"
            else:
                space_type = "chance"
                name = "Chance"
            
            self.spaces.append({
                "name": name,
                "type": space_type,
                "position": position,
                "x": x,
                "y": y
            })
    
    def draw(self, screen):
        # Draw the board background
        pygame.draw.rect(screen, (230, 230, 230), (100, 100, 600, 600))
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 600, 600), 2)
        
        # Draw each space
        for space in self.spaces:
            # Draw space rectangle
            color = self.get_space_color(space["type"])
            pygame.draw.rect(screen, color, (space["x"], space["y"], 60, 60), 0)
            pygame.draw.rect(screen, (0, 0, 0), (space["x"], space["y"], 60, 60), 1)
            
            # Draw space name
            font = pygame.font.SysFont(None, 16)
            text = font.render(space["name"], True, (0, 0, 0))
            text_rect = text.get_rect(center=(space["x"] + 30, space["y"] + 30))
            screen.blit(text, text_rect)
    
    def get_space_color(self, space_type):
        if space_type == "go":
            return (255, 0, 0)  # Red
        elif space_type == "jail":
            return (128, 128, 128)  # Gray
        elif space_type == "free_parking":
            return (0, 255, 0)  # Green
        elif space_type == "go_to_jail":
            return (0, 0, 255)  # Blue
        elif space_type == "property":
            return (255, 255, 200)  # Light yellow
        elif space_type == "chance":
            return (255, 165, 0)  # Orange
        else:
            return (255, 255, 255)  # White
    
    def get_space_position(self, position):
        for space in self.spaces:
            if space["position"] == position:
                return (space["x"] + 30, space["y"] + 30)
        return (0, 0)  # Default if not found

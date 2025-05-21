import pygame

class Player:
    def __init__(self, name, token_color, starting_balance=1500):
        self.name = name
        self.token_color = token_color
        self.position = 0
        self.balance = starting_balance
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
    
    def move(self, steps):
        old_position = self.position
        self.position = (self.position + steps) % 40  # 40 spaces on the board
        
        # Check if passed GO
        if self.position < old_position:
            self.balance += 200  # Collect $200 for passing GO
            return True
        return False
    
    def update_balance(self, amount):
        self.balance += amount
        return self.balance
    
    def is_bankrupt(self):
        return self.balance < 0
    
    def draw(self, screen, board):
        # Get position coordinates from the board
        x, y = board.get_space_position(self.position)
        
        # Draw player token
        pygame.draw.circle(screen, self.token_color, (x, y), 10)
        
        # Draw player name
        font = pygame.font.SysFont(None, 16)
        text = font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y - 15))
        screen.blit(text, text_rect)

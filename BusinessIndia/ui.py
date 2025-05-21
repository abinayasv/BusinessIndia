import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(None, 24)
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class PlayerPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 18)
    
    def draw(self, screen, players, current_player_index):
        pygame.draw.rect(screen, (230, 230, 230), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        title = self.font.render("Players", True, (0, 0, 0))
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        y_offset = 40
        for i, player in enumerate(players):
            # Highlight current player
            if i == current_player_index:
                pygame.draw.rect(screen, (255, 255, 200), 
                                (self.rect.x + 5, self.rect.y + y_offset - 5, 
                                 self.rect.width - 10, 30))
            
            # Draw player token
            pygame.draw.circle(screen, player.token_color, 
                              (self.rect.x + 20, self.rect.y + y_offset + 5), 8)
            
            # Draw player name and balance
            name_text = self.font.render(player.name, True, (0, 0, 0))
            screen.blit(name_text, (self.rect.x + 40, self.rect.y + y_offset))
            
            balance_text = self.small_font.render(f"${player.balance}", True, (0, 0, 0))
            screen.blit(balance_text, (self.rect.x + 40, self.rect.y + y_offset + 20))
            
            y_offset += 50

class PropertyInfoPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 18)
        self.property = None
    
    def set_property(self, property):
        self.property = property
    
    def draw(self, screen, current_player):
        pygame.draw.rect(screen, (230, 230, 230), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        title = self.font.render("Property Info", True, (0, 0, 0))
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        if self.property:
            # Property name
            name_text = self.font.render(self.property.name, True, (0, 0, 0))
            screen.blit(name_text, (self.rect.x + 10, self.rect.y + 40))
            
            # Property price
            price_text = self.small_font.render(f"Price: ${self.property.price}", True, (0, 0, 0))
            screen.blit(price_text, (self.rect.x + 10, self.rect.y + 70))
            
            # Property rent
            rent_text = self.small_font.render(f"Rent: ${self.property.rent_current}", True, (0, 0, 0))
            screen.blit(rent_text, (self.rect.x + 10, self.rect.y + 90))
            
            # Property owner
            owner_text = "Unowned"
            if self.property.owner:
                owner_text = f"Owner: {self.property.owner.name}"
            owner_surface = self.small_font.render(owner_text, True, (0, 0, 0))
            screen.blit(owner_surface, (self.rect.x + 10, self.rect.y + 110))
            
            # Buy button if property is unowned and player has enough money
            if (self.property.owner is None and 
                current_player and 
                current_player.balance >= self.property.price):
                buy_button = Button(
                    self.rect.x + 10, 
                    self.rect.y + 140, 
                    100, 30, 
                    "Buy Property", 
                    (100, 255, 100), 
                    (150, 255, 150)
                )
                buy_button.draw(screen)
                return buy_button
        else:
            no_prop_text = self.small_font.render("No property selected", True, (0, 0, 0))
            screen.blit(no_prop_text, (self.rect.x + 10, self.rect.y + 40))
        
        return None

class DicePanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.dice_value = 0
        self.rolling = False
        self.roll_frames = 0
        self.max_roll_frames = 20
    
    def start_rolling(self):
        self.rolling = True
        self.roll_frames = 0
    
    def update(self):
        if self.rolling:
            self.roll_frames += 1
            if self.roll_frames >= self.max_roll_frames:
                self.rolling = False
    
    def draw(self, screen, dice_value):
        pygame.draw.rect(screen, (230, 230, 230), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        title = self.font.render("Dice", True, (0, 0, 0))
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw dice
        dice_rect = pygame.Rect(self.rect.x + 50, self.rect.y + 40, 60, 60)
        pygame.draw.rect(screen, (255, 255, 255), dice_rect)
        pygame.draw.rect(screen, (0, 0, 0), dice_rect, 2)
        
        if not self.rolling:
            # Draw dice value
            value_text = self.font.render(str(dice_value), True, (0, 0, 0))
            value_rect = value_text.get_rect(center=dice_rect.center)
            screen.blit(value_text, value_rect)
        else:
            # Show animation (simplified)
            value_text = self.font.render("?", True, (0, 0, 0))
            value_rect = value_text.get_rect(center=dice_rect.center)
            screen.blit(value_text, value_rect)
        
        return dice_rect

class MessagePanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.message = ""
        self.message_time = 0
    
    def set_message(self, message):
        self.message = message
        self.message_time = pygame.time.get_ticks()
    
    def draw(self, screen):
        pygame.draw.rect(screen, (230, 230, 230), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        title = self.font.render("Messages", True, (0, 0, 0))
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw message with word wrap
        if self.message:
            words = self.message.split(' ')
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                # Check if the line is too long
                if self.font.size(test_line)[0] > self.rect.width - 20:
                    lines.append(line)
                    line = word + " "
                else:
                    line = test_line
            lines.append(line)  # Add the last line
            
            y_offset = 40
            for line in lines:
                text = self.font.render(line, True, (0, 0, 0))
                screen.blit(text, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 25

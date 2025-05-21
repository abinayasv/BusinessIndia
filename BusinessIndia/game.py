import pygame
import random
from property import Property
from player import Player

class BusinessIndiaGame:
    def __init__(self):
        self.players = []
        self.properties = []
        self.current_player_index = 0
        self.dice_value = 0
        self.game_state = "setup"  # setup, playing, game_over
        self.message = ""
        self.initialize_properties()
    
    def initialize_properties(self):
        # Create properties with Indian states
        states = [
            {"name": "Maharashtra", "position": 1, "price": 400, "rent": 50, "color": "brown"},
            {"name": "Delhi", "position": 3, "price": 350, "rent": 35, "color": "brown"},
            {"name": "West Bengal", "position": 6, "price": 320, "rent": 30, "color": "light_blue"},
            {"name": "Tamil Nadu", "position": 8, "price": 300, "rent": 26, "color": "light_blue"},
            {"name": "Karnataka", "position": 9, "price": 280, "rent": 24, "color": "light_blue"},
            {"name": "Telangana", "position": 11, "price": 260, "rent": 22, "color": "pink"},
            {"name": "Gujarat", "position": 13, "price": 240, "rent": 20, "color": "pink"},
            {"name": "Rajasthan", "position": 14, "price": 220, "rent": 18, "color": "pink"},
            {"name": "Uttar Pradesh", "position": 16, "price": 200, "rent": 16, "color": "orange"},
            {"name": "Bihar", "position": 18, "price": 180, "rent": 14, "color": "orange"},
            {"name": "Madhya Pradesh", "position": 19, "price": 160, "rent": 12, "color": "orange"},
            {"name": "Kerala", "position": 21, "price": 140, "rent": 10, "color": "red"},
            {"name": "Punjab", "position": 23, "price": 140, "rent": 10, "color": "red"},
            {"name": "Haryana", "position": 24, "price": 120, "rent": 8, "color": "red"},
            {"name": "Assam", "position": 26, "price": 100, "rent": 6, "color": "yellow"},
            {"name": "Odisha", "position": 27, "price": 100, "rent": 6, "color": "yellow"},
            {"name": "Chhattisgarh", "position": 29, "price": 120, "rent": 8, "color": "yellow"},
            {"name": "Jharkhand", "position": 31, "price": 140, "rent": 10, "color": "green"},
            {"name": "Uttarakhand", "position": 32, "price": 150, "rent": 12, "color": "green"},
            {"name": "Himachal Pradesh", "position": 34, "price": 160, "rent": 14, "color": "green"},
            {"name": "Goa", "position": 37, "price": 350, "rent": 35, "color": "blue"},
            {"name": "Sikkim", "position": 39, "price": 400, "rent": 50, "color": "blue"},
        ]
        
        # Create property objects
        for state in states:
            self.properties.append(
                Property(
                    state["name"], 
                    state["position"], 
                    state["price"], 
                    state["rent"], 
                    state["color"]
                )
            )
    
    def add_player(self, name, color):
        self.players.append(Player(name, color))
    
    def roll_dice(self):
        return random.randint(1, 6)
    
    def next_turn(self):
        # Check if current player is bankrupt
        if self.players[self.current_player_index].is_bankrupt():
            self.players.pop(self.current_player_index)
            if len(self.players) <= 1:
                self.game_state = "game_over"
                return
        else:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def get_property_at_position(self, position):
        for prop in self.properties:
            if prop.position == position:
                return prop
        return None
    
    def buy_property(self, player, property):
        if property.owner is None and player.balance >= property.price:
            player.update_balance(-property.price)
            property.owner = player
            player.properties.append(property)
            self.message = f"{player.name} bought {property.name} for ${property.price}"
            return True
        elif property.owner is None and player.balance < property.price:
            self.message = f"Not enough money to buy {property.name}"
        return False
    
    def pay_rent(self, player, property):
        if property.owner is not None and property.owner != player and not property.mortgaged:
            rent = property.calculate_rent()
            player.update_balance(-rent)
            property.owner.update_balance(rent)
            self.message = f"{player.name} paid ${rent} rent to {property.owner.name}"
            return rent
        return 0
    
    def handle_player_landed(self):
        current_player = self.get_current_player()
        property = self.get_property_at_position(current_player.position)
        
        if property:
            if property.owner is None:
                # Property is available to buy
                self.message = f"{property.name} is available for ${property.price}"
            elif property.owner != current_player:
                # Pay rent
                self.pay_rent(current_player, property)
            else:
                # Player owns this property
                self.message = f"You own {property.name}"
        elif current_player.position == 0:
            # GO
            self.message = "You landed on GO"
        elif current_player.position == 10:
            # Just visiting jail
            self.message = "Just visiting jail"
        elif current_player.position == 20:
            # Free parking
            self.message = "Free parking"
        elif current_player.position == 30:
            # Go to jail
            current_player.position = 10
            current_player.in_jail = True
            current_player.jail_turns = 3
            self.message = "Go to jail! Do not pass GO, do not collect $200"
        elif current_player.position in [2, 7, 17, 22, 33, 36]:
            # Chance
            self.handle_chance(current_player)
        elif current_player.position in [4, 38]:
            # Income Tax / Luxury Tax
            tax = 200 if current_player.position == 4 else 100
            current_player.update_balance(-tax)
            self.message = f"You paid ${tax} in taxes"
    
    def handle_chance(self, player):
        # Implement chance card logic
        chance_options = [
            {"message": "Bank pays you dividend of $50", "action": lambda p: p.update_balance(50)},
            {"message": "Pay hospital fees of $100", "action": lambda p: p.update_balance(-100)},
            {"message": "Advance to GO", "action": lambda p: setattr(p, 'position', 0) or p.update_balance(200)},
            {"message": "You won a lottery! Collect $150", "action": lambda p: p.update_balance(150)},
            {"message": "Pay school fees of $50", "action": lambda p: p.update_balance(-50)},
            {"message": "Bank error in your favor. Collect $200", "action": lambda p: p.update_balance(200)},
        ]
        
        # Select a random chance card
        chance = random.choice(chance_options)
        chance["action"](player)
        self.message = f"Chance: {chance['message']}"

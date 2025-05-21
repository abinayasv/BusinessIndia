class Property:
    def __init__(self, name, position, price, rent_base, color_group=None):
        self.name = name
        self.position = position
        self.price = price
        self.rent_base = rent_base
        self.rent_current = rent_base
        self.owner = None
        self.houses = 0
        self.hotel = False
        self.color_group = color_group
        self.mortgaged = False
    
    def calculate_rent(self):
        if self.mortgaged:
            return 0
        
        if self.hotel:
            return self.rent_base * 5
        else:
            return self.rent_base * (1 + self.houses)
    
    def add_house(self):
        if self.houses < 4 and not self.hotel:
            self.houses += 1
            self.rent_current = self.calculate_rent()
            return True
        return False
    
    def add_hotel(self):
        if self.houses == 4 and not self.hotel:
            self.houses = 0
            self.hotel = True
            self.rent_current = self.calculate_rent()
            return True
        return False
    
    def mortgage(self):
        if not self.mortgaged and self.houses == 0 and not self.hotel:
            self.mortgaged = True
            return self.price // 2  # Return mortgage value
        return 0
    
    def unmortgage(self):
        if self.mortgaged:
            self.mortgaged = False
            return int(self.price * 0.55)  # Return unmortgage cost (50% + 10% interest)
        return 0

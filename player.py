class Player:
    def __init__(self):
        # Starting resources
        self.coins = 500
        self.lives = 20
        self.score = 0

    def can_afford(self, cost):
        return self.coins >= cost

    def spend_coins(self, amount):
        if self.can_afford(amount):
            self.coins -= amount
            return True
        return False

    def add_coins(self, amount):
        self.coins += amount

    def lose_life(self, amount=1):
        self.lives -= amount

    def add_score(self, amount):
        self.score += amount
from .dice_roller import DiceRoller

class Character:
    def __init__(self, name, dice_count):
        self.name = name
        self.dice_count = dice_count
        self.hp = self.roll_starting_hp()
        self.shield = 0
        self.card = None
        self.life_steal = False
        self.damage_penalty = 0

    def roll_starting_hp(self):
        return sum(DiceRoller.roll(self.dice_count))

    def take_damage(self, amount):
        if self.shield > 0:
            blocked = min(self.shield, amount)
            self.shield -= blocked
            amount -= blocked
            print(f"{self.name}'s shield blocks {blocked} damage!")
        if amount > 0:
            self.hp -= amount

    def is_alive(self):
        return self.hp > 0
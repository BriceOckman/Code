import random

class DiceRoller:
    @staticmethod
    def roll(num):
        return [random.randint(1, 6) for _ in range(num)]
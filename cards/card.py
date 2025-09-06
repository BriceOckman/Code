from game.dice_roller import DiceRoller
from .card_id import CardID
from .card_effect import CardEffect

class Card:
    def __init__(self, card_id):
        self.card_id = card_id
        self.used = False

    def description(self):
        descs = {
            1: "Heal 2 HP",
            2: "Roll die. Player gains shield equivalent to that roll.",
            3: "On turn, heal HP equal to damage dealt. If the player loses or ties, the house’s damage receives an additional +1",
            4: "Create shield equivalent to 4, at expense of -1 to damage.",
            5: "Roll die. On 4-6, boss takes that much extra damage. On 1-3, player takes that much extra damage.",
            6: "Roll two die. If sum > 8, deal 6 damage to the boss. If < 7, take that damage."
        }
        return descs[self.card_id]

    def use(self, game, who="player"):
        if self.used:
            print("Card already used.")
            return
        actor = game.player if who == "player" else game.boss
        target = game.boss if who == "player" else game.player
        CardEffect.apply(self.card_id, game, actor, target)
        self.used = True
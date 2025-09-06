from .dice_roller import DiceRoller
from cards.card import Card
from .character import Character
from .game_io import GameIO
import time

class DiceGame:
    """
    Main class for managing the Dice Boss Battle game.
    Handles game setup, turns, player and boss actions, and win/loss conditions.
    """

    def __init__(self, io=None):
        """
        Initialize the DiceGame with optional custom I/O handler.
        Sets up player, boss, and game state.
        """
        self.io = io or GameIO()
        self.player = Character("Player", 2)
        self.boss = Character("Boss", 6)
        self.turn = 1
        self.last_player_roll = None
        self.last_boss_roll = None

    def explain_rules(self):
        """
        Print the game rules to the player.
        """
        self.io.print("Welcome to the Dice Boss Battle!")
        self.io.print("Rules:")
        self.io.print("1. You roll two dice each turn. The house rolls one die.")
        self.io.print("2. If your roll is higher than the house, you deal the difference as damage to the boss.")
        self.io.print("3. If you tie with the house, you take damage equal to the house's roll.")
        self.io.print("4. If the house rolls higher, you take damage equal to the house's roll.")
        self.io.print("5. Your HP is the sum of your first two dice rolls.")
        self.io.print("6. The boss's HP is the sum of six dice rolls.")
        self.io.print("7. If you roll doubles, you draw a card (single use, can be saved for later).")
        self.io.print("Good luck!\n")

    def display_starting_hp(self):
        """
        Display the starting HP for both player and boss.
        """
        self.io.input("Press Enter to roll your dice...")
        self.io.print(f"Rolling player's HP: --")
        time.sleep(1)
        self.io.print(f"Your starting HP: {self.player.hp}")
        self.io.print(f"Rolling Boss's HP: --")
        time.sleep(1)
        self.io.print(f"Boss starting HP: {self.boss.hp}\n")

    def draw_card(self, who="player"):
        """
        Draw a card for the player or boss and display its description.
        Returns:
            Card: The drawn card object.
        """
        card_id = DiceRoller.roll(1)[0]
        card = Card(card_id)
        if who == "player":
            self.io.print(f"You drew a card: {card.description()}")
        else:
            self.io.print(f"Boss drew a card: {card.description()}")
        return card

    def ask_use_card(self):
        """
        Ask the player if they want to use their card, and use it if confirmed.
        """
        if self.player.card and not self.player.card.used:
            self.io.print(f"You have a card: {self.player.card.description()}")
            use = self.io.input("Use your card now? (y/n): ").strip().lower()
            if use == "y":
                self.player.card.use(self)
                self.player.card = None

    def player_turn(self, mode="normal"):
        """
        Handle the player's turn, including rolling dice and card logic.
        Args:
            mode (str): The mode for this turn ("normal", "defend", or "risk").
        Returns:
            tuple: (player_roll, rolls)
        """
        self.ask_use_card()
        self.io.input("Press Enter to roll your dice...")
        dice_count = 2
        if mode == "defend":
            dice_count = 1
        elif mode == "risk":
            dice_count = 3
        rolls = DiceRoller.roll(dice_count)
        player_roll = sum(rolls)
        self.last_player_roll = player_roll
        self.io.print(f"Rolling player's Dice: {rolls}")
        time.sleep(1)
        self.io.print(f"You rolled: {player_roll} ({dice_count} dice)")

        if mode == "defend" and 6 in rolls:
            self.io.print("You rolled a 6 while defending! You draw a card.")
            self.player.card = self.draw_card("player")

        if mode != "defend" and len(rolls) >= 2 and len(set(rolls)) == 1 and not self.player.card:
            self.io.print("You rolled doubles!")
            self.player.card = self.draw_card("player")
            use_now = self.io.input("Use card now? (y/n): ").strip().lower()
            if use_now == "y":
                self.player.card.use(self)
                self.player.card = None

        return player_roll, rolls

    def boss_turn(self, mode="normal"):
        """
        Handle the boss's turn, including rolling dice and card logic.
        Args:
            mode (str): The mode for this turn ("normal" or "risk").
        Returns:
            tuple: (boss_roll, boss_rolls)
        """
        self.io.print("Boss's turn...")
        time.sleep(1)
        dice_count = 1
        if mode == "risk":
            dice_count = 2
        boss_rolls = DiceRoller.roll(dice_count)
        boss_roll = sum(boss_rolls)
        self.last_boss_roll = boss_roll
        self.io.print(f"Boss rolled: {boss_rolls} ({dice_count} die{'s' if dice_count > 1 else ''})")

        if mode == "normal" and 1 in boss_rolls:
            self.io.print("Boss rolled a 1!")
            self.boss.card = self.draw_card("boss")
            self.io.print("Boss uses their card immediately!")
            self.boss.card.use(self, who="boss")
            self.boss.card = None
        elif mode == "risk" and len(boss_rolls) == 2 and boss_rolls[0] == boss_rolls[1]:
            self.io.print("Boss rolled doubles!")
            self.boss.card = self.draw_card("boss")
            self.io.print("Boss uses their card immediately!")
            self.boss.card.use(self, who="boss")
            self.boss.card = None

        return boss_roll, boss_rolls

    def resolve_turn(self, player_roll, boss_roll, mode="normal", player_rolls=None, boss_rolls=None):
        """
        Resolve the outcome of a turn based on player and boss rolls and mode.
        Args:
            player_roll (int): The player's total roll.
            boss_roll (int): The boss's total roll.
            mode (str): The mode for this turn.
            player_rolls (list): Individual dice rolls for the player.
            boss_rolls (list): Individual dice rolls for the boss.
        """
        damage_penalty = self.player.damage_penalty
        self.player.damage_penalty = 0
        life_steal = self.player.life_steal
        self.player.life_steal = False

        if mode == "defend":
            if player_roll == boss_roll:
                self.io.print("You matched the boss's roll! No damage taken.")
            else:
                damage = boss_roll // 2
                self.player.take_damage(damage)
                self.io.print(f"You defended! You take only {damage} damage.")
        else:
            if player_roll > boss_roll:
                damage = player_roll - boss_roll - damage_penalty
                damage = max(0, damage)
                self.boss.take_damage(damage)
                self.io.print(f"You hit the boss for {damage} damage!")
                if life_steal:
                    self.player.hp += damage
                    self.io.print(f"You heal {damage} HP from life steal!")
            else:
                damage = boss_roll
                if life_steal:
                    damage += 1
                self.player.take_damage(damage)
                self.io.print(f"The house hits you for {damage} damage!")

        time.sleep(1)
        self.io.print(f"Your HP: {self.player.hp} (Shield: {self.player.shield})")
        self.io.print(f"Boss HP: {self.boss.hp}\n")

    def play(self):
        """
        Main game loop. Handles turn progression and win/loss conditions.
        """
        self.explain_rules()
        self.display_starting_hp()
        while self.player.is_alive() and self.boss.is_alive():
            self.io.print(f"--- Turn {self.turn} ---")
            time.sleep(0.5)
            mode = "normal"
            while True:
                choice = self.io.input("Choose your action (defend/risk/normal): ").strip().lower()
                if choice in ("defend", "risk", "normal", ""):
                    mode = choice if choice else "normal"
                    break
                self.io.print("Invalid choice. Please enter 'defend', 'risk', or press Enter for normal.")
            player_roll, player_rolls = self.player_turn(mode)
            boss_roll, boss_rolls = self.boss_turn(mode)
            self.resolve_turn(player_roll, boss_roll, mode, player_rolls, boss_rolls)
            self.turn += 1
        if not self.player.is_alive():
            self.io.print("You lost! The boss wins.")
        else:
            self.io.print("You win! The boss is defeated.")


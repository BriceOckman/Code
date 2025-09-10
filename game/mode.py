
from dice_roller import DiceRoller
import time

class Mode:
    """
    Base class for game modes.
    """
    name = "base"

    def get_player_dice_count(self):
        return 2

    def get_boss_dice_count(self):
        return 1

    def player_special(self, game, rolls):
        """Handle special effects for player rolls."""
        pass

    def boss_special(self, game, rolls):
        """Handle special effects for boss rolls."""
        pass

    def resolve(self, game, player_roll, boss_roll, player_rolls=None, boss_rolls=None):
        """Resolve the outcome of a turn."""
        pass

class NormalMode(Mode):
    name = "normal"

    def player_special(self, game, rolls):
        # Doubles: draw card if not already holding one
        if len(rolls) >= 2 and len(set(rolls)) == 1 and not game.player.card:
            game.io.print("You rolled doubles!")
            game.player.card = game.draw_card("player")
            use_now = game.io.input("Use card now? (y/n): ").strip().lower()
            if use_now == "y":
                game.player.card.use(game)
                game.player.card = None

    def boss_special(self, game, rolls):
        # Boss rolls a 1: draw and use card
        if 1 in rolls:
            game.io.print("Boss rolled a 1!")
            game.boss.card = game.draw_card("boss")
            game.io.print("Boss uses their card immediately!")
            game.boss.card.use(game, who="boss")
            game.boss.card = None

    def resolve(self, game, player_roll, boss_roll, player_rolls=None, boss_rolls=None):
        damage_penalty = game.player.damage_penalty
        game.player.damage_penalty = 0
        life_steal = game.player.life_steal
        game.player.life_steal = False
        if player_roll > boss_roll:
            damage = player_roll - boss_roll - damage_penalty
            damage = max(0, damage)
            game.boss.take_damage(damage)
            game.io.print(f"You hit the boss for {damage} damage!")
            if life_steal:
                game.player.hp += damage
                game.io.print(f"You heal {damage} HP from life steal!")
        else:
            damage = player_roll - boss_roll
            if life_steal:
                damage += 1
            game.player.take_damage(damage)
            game.io.print(f"The house hits you for {damage} damage!")
        time.sleep(1)
        game.io.print(f"Your HP: {game.player.hp} (Shield: {game.player.shield})")
        game.io.print(f"Boss HP: {game.boss.hp}\n")

class RiskMode(NormalMode):
    name = "risk"

    def get_player_dice_count(self):
        return 3

    def get_boss_dice_count(self):
        return 2

    def player_special(self, game, rolls):
        # Doubles or triples: draw card if not already holding one
        if len(rolls) >= 2 and len(set(rolls)) == 1 and not game.player.card:
            game.io.print("You rolled doubles!")
            game.player.card = game.draw_card("player")
            use_now = game.io.input("Use card now? (y/n): ").strip().lower()
            if use_now == "y":
                game.player.card.use(game)
                game.player.card = None

    def boss_special(self, game, rolls):
        # Boss rolls doubles: draw and use card
        if len(rolls) == 2 and rolls[0] == rolls[1]:
            game.io.print("Boss rolled doubles!")
            game.boss.card = game.draw_card("boss")
            game.io.print("Boss uses their card immediately!")
            game.boss.card.use(game, who="boss")
            game.boss.card = None

    def resolve(self, game, player_roll, boss_roll, player_rolls=None, boss_rolls=None):
        damage_penalty = game.player.damage_penalty
        game.player.damage_penalty = 0
        life_steal = game.player.life_steal
        game.player.life_steal = False
        # In risk mode, if player wins, deal double damage, if boss wins, deal full boss roll as damage
        if player_roll > boss_roll:
            damage = (player_roll - boss_roll - damage_penalty) * 2
            damage = max(0, damage)
            game.boss.take_damage(damage)
            game.io.print(f"You hit the boss for {damage} RISK damage!")
            if life_steal:
                game.player.hp += damage
                game.io.print(f"You heal {damage} HP from life steal!")
        else:
            damage = 2 * (boss_roll - player_roll)
            if life_steal:
                damage += 2  # risk mode: more punishment for losing
            game.player.take_damage(damage)
            game.io.print(f"The house hits you for {damage} RISK damage!")
        time.sleep(1)
        game.io.print(f"Your HP: {game.player.hp} (Shield: {game.player.shield})")
        game.io.print(f"Boss HP: {game.boss.hp}\n")

class DefendMode(Mode):
    name = "defend"

    def get_player_dice_count(self):
        return 1

    def player_special(self, game, rolls):
        # Roll a 6: draw card
        if 6 in rolls:
            game.io.print("You rolled a 6 while defending! You draw a card.")
            game.player.card = game.draw_card("player")

    def resolve(self, game, player_roll, boss_roll, player_rolls=None, boss_rolls=None):
        damage_penalty = game.player.damage_penalty
        game.player.damage_penalty = 0
        life_steal = game.player.life_steal
        game.player.life_steal = False
        # In defend mode, if player matches boss, no damage. Otherwise, take half boss roll (rounded down)
        if player_roll == boss_roll:
            game.io.print("You matched the boss's roll! No damage taken.")
        elif (player_roll > boss_roll):
            damage = boss_roll - player_roll
            game.boss.take_damage(damage)
            game.io.print(f"You hit the boss for {damage} damage!")
        else:
            damage = (player_roll - boss_roll) // 2
            game.player.take_damage(damage)
            game.io.print(f"You defended! You take only {damage} damage.")
        time.sleep(1)
        game.io.print(f"Your HP: {game.player.hp} (Shield: {game.player.shield})")
        game.io.print(f"Boss HP: {game.boss.hp}\n")

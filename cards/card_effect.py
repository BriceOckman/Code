from game.dice_roller import DiceRoller
from .card_id import CardID

class CardEffect:
    @staticmethod
    def apply(card_id, game, actor, target):
        if card_id == CardID.HEAL:
            actor.hp += 2
            print(f"{actor.name} heals 2 HP!")

        elif card_id == CardID.SHIELD:
            shield = DiceRoller.roll(1)[0]
            actor.shield += shield
            print(f"{actor.name} gains a shield of {shield}!")

        elif card_id == CardID.LIFE_STEAL:
            actor.life_steal = True
            print(f"Life Steal active for {actor.name} this turn!")

        elif card_id == CardID.SHIELD_PENALTY:
            actor.shield += 4
            actor.damage_penalty = 1
            print(f"{actor.name} gains a shield of 4, but -1 to their damage this turn.")
            
        elif card_id == CardID.DAMAGE_CHANCE:
            roll = DiceRoller.roll(1)[0]
            if roll >= 4:
                target.take_damage(roll)
                print(f"{target.name} takes {roll} extra damage!")
            else:
                actor.take_damage(roll)
                print(f"{actor.name} takes {roll} extra damage!")

        elif card_id == CardID.DOUBLE_ROLL:
            roll = sum(DiceRoller.roll(2))
            if actor.name == "Player":
                if roll > 8:
                    target.take_damage(6)
                    print("You deal 6 damage to the boss!")
                elif roll < 7:
                    actor.take_damage(roll)
                    print(f"You take {roll} damage!")
                else:
                    print("No effect.")
            else:
                if roll > 8:
                    target.take_damage(6)
                    print("Boss deals 6 damage to you!")
                elif roll < 7:
                    actor.take_damage(roll)
                    print(f"Boss takes {roll} damage!")
                else:
                    print("No effect.")
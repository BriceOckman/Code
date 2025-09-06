# Dice Boss Battle

## Overview

Dice Boss Battle is a turn-based dice game where you face off against a boss in a battle of luck, strategy, and special cards. Roll dice, draw cards, and use their effects to defeat the boss before your HP runs out!

## Rules

1. **Starting HP**:
   - The player rolls two dice; the sum is their starting HP.
   - The boss rolls six dice; the sum is their starting HP.

2. **Turns**:
   - Each turn, the player and the boss roll dice.
   - The player chooses an action: `normal`, `defend`, or `risk`.
     - **Normal**: Player rolls 2 dice, boss rolls 1 die.
     - **Defend**: Player rolls 1 die, boss rolls 1 die. If the player matches the boss's roll, no damage is taken; otherwise, the player takes half the boss's roll as damage.
     - **Risk**: Player rolls 3 dice, boss rolls 2 dice.

3. **Damage**:
   - If the player's roll is higher, the boss takes damage equal to the difference.
   - If the rolls are tied, the player takes damage equal to the boss's roll.
   - If the boss's roll is higher, the player takes damage equal to the boss's roll.

4. **Cards**:
   - If the player rolls doubles (all dice show the same number), they draw a card.
   - Cards have special effects and can be used immediately or saved for later (one at a time).
   - The boss can also draw and use cards under certain conditions.

5. **Card Effects**:
   - Heal, shield, life steal, damage chance, and more. See in-game descriptions for details.

6. **Winning and Losing**:
   - The game continues until either the player or the boss's HP drops to zero.
   - If the player survives and the boss is defeated, the player wins. Otherwise, the boss wins.

## How to Play

1. **Run the Game**  
   From the project directory, run:
   ```sh
   python main.py
   ```

2. **Follow Prompts**  
   - Read the rules and press Enter to roll for starting HP.
   - On each turn, choose your action: `defend`, `risk`, or press Enter for normal.
   - Roll dice and resolve the outcome.
   - Use cards when prompted.

3. **Strategy**  
   - Use defend to reduce damage.
   - Take risks for higher potential damage (and danger).
   - Use cards wisely to turn the tide of
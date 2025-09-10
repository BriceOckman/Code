# Dice Boss Battle

## Overview

Dice Boss Battle is a turn-based dice game where you face off against a boss in a battle of luck, strategy, and special cards. Roll dice, draw cards, and use their effects to defeat the boss before your HP runs out!

## Game Setup

- **Player HP**: Roll 2 dice; the sum is your starting HP.
- **Boss HP**: Roll 6 dice; the sum is the boss's starting HP.

## Turn Structure

Each turn, you choose an action mode and both you and the boss roll dice according to the mode:

### Modes

- **Normal**
   - Player rolls 2 dice, boss rolls 1 die.
   - If player rolls doubles (both dice the same), draw a card.
   - If boss rolls a 1, boss draws and immediately uses a card.
   - **Damage**:
      - If player total > boss total: Boss takes (player - boss) damage.
      - If boss total >= player total: Player takes (player - boss) damage (may be negative, i.e., player heals if boss rolls lower).

- **Risk**
   - Player rolls 3 dice, boss rolls 2 dice.
   - If player rolls all the same (doubles/triples), draw a card.
   - If boss rolls doubles, boss draws and immediately uses a card.
   - **Damage**:
      - If player total > boss total: Boss takes 2 × (player - boss) damage.
      - If boss total >= player total: Player takes 2 × (boss - player) damage.

- **Defend**
   - Player rolls 1 die, boss rolls 1 die.
   - If player rolls a 6, draw a card.
   - **Damage**:
      - If player matches boss: No damage to either.
      - If player > boss: Boss takes (boss - player) damage (may be negative, i.e., boss heals if player rolls much higher).
      - If boss > player: Player takes half the difference (rounded down): (player - boss) // 2 damage (may be negative, i.e., player heals if boss rolls much higher).

## Cards

- If you roll doubles (or triples in risk mode), you draw a card (if you don't already have one).
- Cards have special effects (heal, shield, life steal, etc.).
- You can use a card immediately or save it for later (only one card at a time).
- The boss can also draw and use cards under certain conditions (see above).

## Card Effects

- Card effects include healing, shields, life steal, bonus damage, and more. See in-game card descriptions for details.

## Winning and Losing

- The game continues until either the player or the boss's HP drops to zero.
- If the player survives and the boss is defeated, the player wins. Otherwise, the boss wins.

## How to Play

1. **Run the Game**
    ```sh
    python main.py
    ```
2. **Follow Prompts**
    - Read the rules and press Enter to roll for starting HP.
    - On each turn, choose your action: `defend`, `risk`, or press Enter for normal.
    - Roll dice and resolve the outcome.
    - Use cards when prompted.
3. **Strategy**
    - Use defend to reduce or avoid damage.
    - Take risks for higher potential damage (and danger).
    - Use cards wisely to turn the tide of battle.
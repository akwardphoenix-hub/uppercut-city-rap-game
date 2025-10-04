from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from .models import Rapper


@dataclass
class BattleLog:
    rounds: int = 0
    transcript: list[str] = None

    def __post_init__(self) -> None:
        if self.transcript is None:
            self.transcript = []


class RapBattle:
    """
    Rhythm battle. Each round:
      - Randomly choose attacker/defender.
      - Attacker rolls accuracy; defender rolls accuracy (for block).
      - If attacker has SPECIAL, they can fire it (ignores block).
      - Otherwise compute damage from move & accuracy; defender may block.
    """

    def __init__(self, r1: Rapper, r2: Rapper, *, seed: Optional[int] = None) -> None:
        # If you pass seeded rappers, this seed isn't needed; here for convenience.
        self.r1 = r1
        self.r2 = r2
        self.log = BattleLog()

    def _round(self) -> None:
        # lightweight "initiative"
        if attacker_first(self.r1, self.r2):
            attacker, defender = self.r1, self.r2
        else:
            attacker, defender = self.r2, self.r1

        # SPECIAL?
        if attacker.special_ready:
            dmg = attacker.special_move()
            defender.hp -= dmg
            self.log.transcript.append(f"🌟 {attacker.name} SPECIAL for {dmg}!")
        else:
            acc_a = attacker.roll_accuracy()
            acc_d = defender.roll_accuracy()
            move_name, damage = attacker.spit_bar(acc_a)
            if defender.defend(acc_d):
                msg = f"🛡️ {defender.name} blocked {attacker.name}'s {move_name}!"
                self.log.transcript.append(msg)
            else:
                defender.hp -= damage
                self.log.transcript.append(f"🎤 {attacker.name} lands {move_name} for {damage}!")

        self.log.rounds += 1

    def play(self, *, sleep: float = 0.0, max_rounds: int = 60) -> str:
        while self.r1.hp > 0 and self.r2.hp > 0 and self.log.rounds < max_rounds:
            self._round()
            if sleep:
                time.sleep(sleep)

        winner = self.r1 if self.r1.hp > 0 else self.r2
        loser = self.r2 if winner is self.r1 else self.r1
        winner.gain_xp(3)
        msg = f"🏆 {winner.name} defeats {loser.name} in {self.log.rounds} rounds!"
        self.log.transcript.append(msg)
        return winner.name


def attacker_first(a: Rapper, b: Rapper) -> bool:
    # Slight bias to higher accuracy; break ties randomly via each RNG
    bias_a = a.base_accuracy + a.accuracy_bonus + a.rng.random() * 0.1
    bias_b = b.base_accuracy + b.accuracy_bonus + b.rng.random() * 0.1
    return bias_a >= bias_b

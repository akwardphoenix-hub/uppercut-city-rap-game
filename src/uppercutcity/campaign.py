from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from .battle import RapBattle
from .models import Rapper, load_json


@dataclass
class MatchResult:
    district: str
    stage: str  # warmup | midboss | boss
    winner: str
    transcript: List[str]


class Campaign:
    """
    District ladder: each district has [warmups...], a midboss, and a boss.
    Rewards: XP + unlock gear or characters as specified in districts.json.
    """

    def __init__(self, player: Rapper, *, rng: Optional[random.Random] = None) -> None:
        self.player = player
        self.rng = rng or random.Random()
        self.districts = load_json("districts.json")
        self.unlocks: Dict[str, bool] = {}

    def _enemy(self, name: str) -> Rapper:
        # seed enemy RNG independently for determinism per run
        enemy_rng = random.Random(self.rng.randint(0, 999999))
        return Rapper.from_catalog(name, rng=enemy_rng)

    def run(self) -> List[MatchResult]:
        results: List[MatchResult] = []
        for d in self.districts:
            # warmups
            for name in d["warmups"]:
                enemy = self._enemy(name)
                battle = RapBattle(self.player, enemy)
                winner = battle.play()
                result = MatchResult(
                    d["id"], "warmup", winner, battle.log.transcript.copy()
                )
                results.append(result)
            # midboss
            enemy = self._enemy(d["midboss"])
            battle = RapBattle(self.player, enemy)
            winner = battle.play()
            result = MatchResult(
                d["id"], "midboss", winner, battle.log.transcript.copy()
            )
            results.append(result)
            # boss
            enemy = self._enemy(d["boss"])
            battle = RapBattle(self.player, enemy)
            winner = battle.play()
            result = MatchResult(
                d["id"], "boss", winner, battle.log.transcript.copy()
            )
            results.append(result)
            # rewards
            self._apply_rewards(d)
        return results

    def _apply_rewards(self, district: Dict) -> None:
        rewards = district.get("rewards", {})
        # unlock character(s)
        for char in rewards.get("unlock_characters", []):
            self.unlocks[f"char:{char}"] = True
        # unlock gear IDs (player auto-equips first time if slot empty)
        for gear_id in rewards.get("unlock_gear", []):
            self.unlocks[f"gear:{gear_id}"] = True

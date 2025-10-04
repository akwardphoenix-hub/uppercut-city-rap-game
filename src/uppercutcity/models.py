from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def load_json(name: str):
    with open(DATA / name, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------- Content primitives ----------

@dataclass
class Move:
    id: str
    name: str
    base_damage: int

    @staticmethod
    def from_dict(d: Dict) -> "Move":
        return Move(id=d["id"], name=d["name"], base_damage=int(d["base_damage"]))


@dataclass
class Gear:
    id: str
    slot: str  # mic | hoodie | kicks
    name: str
    mods: Dict[str, float]  # attack|defense|accuracy bonuses in [0..1] deltas

    @staticmethod
    def from_dict(d: Dict) -> "Gear":
        return Gear(id=d["id"], slot=d["slot"], name=d["name"], mods=dict(d["mods"]))


# ---------- Game entities ----------

@dataclass
class Rapper:
    name: str
    hp: int = 15
    level: int = 1
    xp: int = 0
    base_accuracy: float = 0.6  # average rhythm sense
    base_defense: float = 0.15  # chance to block (vs defender accuracy)
    combo_meter: int = 0
    special_ready: bool = False
    rng: random.Random = field(default_factory=random.Random)

    # cosmetic & loadout
    moveset: List[Move] = field(default_factory=list)
    gear: Dict[str, Gear] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.max_hp = self.hp

    # ---- Derived stats ----
    @property
    def accuracy_bonus(self) -> float:
        return sum(g.mods.get("accuracy", 0.0) for g in self.gear.values())

    @property
    def attack_bonus(self) -> float:
        return sum(g.mods.get("attack", 0.0) for g in self.gear.values())

    @property
    def defense_bonus(self) -> float:
        return sum(g.mods.get("defense", 0.0) for g in self.gear.values())

    # ---- Core actions ----
    def roll_accuracy(self) -> float:
        """Simulate timing near the beat, modified by accuracy bonuses."""
        base = self.base_accuracy + self.accuracy_bonus
        noise = self.rng.uniform(-0.25, 0.25)  # a little human variance
        return max(0.0, min(1.0, base + noise))

    def choose_move(self) -> Move:
        return self.moveset[self.rng.randrange(len(self.moveset))]

    def spit_bar(self, acc: float) -> Tuple[str, int]:
        move = self.choose_move()
        multiplier = 0.5 + 1.5 * acc  # 0.5x..2.0x
        # attack bonus scales damage multiplicatively
        dmg = math.ceil(move.base_damage * multiplier * (1.0 + self.attack_bonus))

        # combo logic
        if acc >= 0.85:
            self.combo_meter += 1
        else:
            self.combo_meter = max(0, self.combo_meter - 1)
        if self.combo_meter >= 3:
            self.special_ready = True

        return (move.name, dmg)

    def special_move(self) -> int:
        if not self.special_ready:
            return 0
        self.special_ready = False
        self.combo_meter = 0
        # special ignores block; scales with level
        return 6 + self.level

    def defend(self, defender_acc: float) -> bool:
        base_chance = 0.35 + self.base_defense + self.defense_bonus
        chance = min(0.95, max(0.05, defender_acc * base_chance))
        return self.rng.random() < chance

    # ---- Progression ----
    def gain_xp(self, amount: int) -> None:
        self.xp += amount
        while self.xp >= 5 * self.level:
            self.level += 1
            self.max_hp += 2
            self.hp = self.max_hp

    # ---- Load helpers ----
    @staticmethod
    def from_catalog(name: str, rng: Optional[random.Random] = None) -> "Rapper":
        chars = load_json("characters.json")
        if name not in chars:
            raise KeyError(f"Unknown character '{name}'")
        spec = chars[name]
        moves = [Move.from_dict(m) for m in load_json("moves.json")[spec["moveset"]]]
        gear_catalog = {g["id"]: Gear.from_dict(g) for g in load_json("gear.json")}
        gear = {slot: gear_catalog[item_id] for slot, item_id in spec.get("gear", {}).items()}
        r = Rapper(
            name=name,
            hp=spec.get("hp", 15),
            level=spec.get("level", 1),
            base_accuracy=spec.get("base_accuracy", 0.6),
            base_defense=spec.get("base_defense", 0.15),
            moveset=moves,
            gear=gear,
            rng=rng or random.Random(),
        )
        return r

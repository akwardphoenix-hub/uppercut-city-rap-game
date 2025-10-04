import random

from uppercutcity.battle import RapBattle
from uppercutcity.models import Rapper


def test_battle_plays_and_returns_winner():
    rng1 = random.Random(42)
    rng2 = random.Random(1337)
    r1 = Rapper.from_catalog("MC Blaze", rng=rng1)
    r2 = Rapper.from_catalog("DJ Uppercut", rng=rng2)
    battle = RapBattle(r1, r2)
    winner = battle.play(sleep=0.0, max_rounds=40)
    assert winner in (r1.name, r2.name)
    assert battle.log.rounds > 0

from uppercutcity.models import Rapper
from uppercutcity.battle import RapBattle
from uppercutcity.campaign import Campaign


def demo_battle():
    print("\n=== Quick Battle ===")
    blaze = Rapper.from_catalog("MC Blaze")
    uppercut = Rapper.from_catalog("DJ Uppercut")
    b = RapBattle(blaze, uppercut)
    winner = b.play(sleep=0.0)
    print("\n".join(b.log.transcript))
    print(f"Winner: {winner}")


def demo_campaign():
    print("\n=== Campaign Run ===")
    hero = Rapper.from_catalog("MC Blaze")
    camp = Campaign(hero)
    results = camp.run()
    for r in results:
        print(f"[{r.district}:{r.stage}] → {r.winner}")
    print(f"Unlocks: {sorted(camp.unlocks.keys())}")


if __name__ == "__main__":
    demo_battle()
    demo_campaign()

from uppercutcity.campaign import Campaign
from uppercutcity.models import Rapper


def test_campaign_runs_and_unlocks_something():
    hero = Rapper.from_catalog("MC Blaze")
    camp = Campaign(hero)
    results = camp.run()
    assert len(results) >= 6  # 2 districts * (1 warmup + midboss + boss)
    # Should record some unlocks from district rewards
    assert any(key.startswith("gear:") for key in camp.unlocks.keys())

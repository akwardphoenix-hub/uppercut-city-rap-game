from uppercutcity.models import Rapper


def test_level_up_and_special_flow():
    r = Rapper.from_catalog("MC Blaze")
    r.gain_xp(20)
    assert r.level >= 2
    r.combo_meter = 3
    r.special_ready = True
    dmg = r.special_move()
    assert dmg >= 7  # 6 + level

# Uppercut City — Rhythm Rap-Fighter 🎶🥊

Fast, funny, and expressive: land bars **on beat** to deal damage, build a **combo meter** for
SPECIALS, and climb the city's districts — **Uptown → Neon Blocks → Dockyard → Highrise** —
to dethrone the boss.

## Features
- Rhythm accuracy → damage multiplier
- Combo meter → Special moves
- XP & level-ups (heal to full on level up)
- Gear (mic, hoodie, kicks) with stat buffs
- District campaign with mid-boss & boss per district
- Deterministic tests + GitHub Actions CI

## Quick start
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Run tests & lint:
```bash
pytest -q
flake8
```

## Files

- `src/uppercutcity/models.py` — core data classes (Rapper, Gear, Move)
- `src/uppercutcity/battle.py` — RapBattle engine (rhythm, damage, specials)
- `src/uppercutcity/campaign.py` — District campaign
- `src/uppercutcity/data/*.json` — content packs (characters, moves, gear, districts)

## Design

Accuracy in [0..1]. Damage = base * (0.5 + 1.5*acc) minus defender block.

Perfects (>0.85) increase combo; combo >= 3 unlocks SPECIAL.

SPECIAL = 6 + level, ignores block.

XP thresholds: need = 5 * level. Level up → max_hp += 2, restore to full.

---

Enjoy. Add districts, rivals, or new gear just by editing JSON. 🎛️

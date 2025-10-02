"""
Battle Mode - Compete against AI opponents in rap battles.
"""

import json
import random


def load_prompts():
    """Load battle prompts from data file."""
    try:
        with open('data/prompts.json', 'r') as f:
            data = json.load(f)
            return data.get('battle_prompts', [])
    except FileNotFoundError:
        return ["Diss your opponent's style", "Boast about your skills"]


def load_rhymes():
    """Load rhyme dictionary."""
    try:
        with open('data/rhymes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def ai_opponent_bar():
    """Generate a simple AI opponent bar."""
    opponent_bars = [
        "My rhymes are fire, yours are weak!",
        "Step aside, I'm the king of this beat!",
        "You can't compete with my lyrical heat!",
        "I'm the champion, accept defeat!"
    ]
    return random.choice(opponent_bars)


def judge_round(player_bar, ai_bar):
    """Simple judging mechanism."""
    # Simple scoring based on length and presence of rhymes
    player_score = len(player_bar.split())
    ai_score = len(ai_bar.split())
    
    if player_score > ai_score:
        return "player"
    elif ai_score > player_score:
        return "ai"
    else:
        return "tie"


def start_battle():
    """Start a rap battle."""
    print("🥊 BATTLE MODE 🥊")
    print("=" * 60)
    print("Time to face off against an opponent!")
    
    prompts = load_prompts()
    player_score = 0
    ai_score = 0
    rounds = 3
    
    print(f"\n⚔️ Best of {rounds} rounds! ⚔️\n")
    
    for round_num in range(1, rounds + 1):
        print(f"\n🎤 ROUND {round_num} 🎤")
        print("-" * 60)
        
        # Give prompt
        prompt = random.choice(prompts) if prompts else "Rap your best bars!"
        print(f"🎯 Theme: {prompt}")
        
        # Player's turn
        print("\n🎵 Your turn! Drop your bars:")
        player_bar = input("🎤 ")
        
        if not player_bar.strip():
            player_bar = "..."
        
        # AI's turn
        print("\n🤖 Opponent's response:")
        ai_bar = ai_opponent_bar()
        print(f"🎤 {ai_bar}")
        
        # Judge
        winner = judge_round(player_bar, ai_bar)
        
        if winner == "player":
            print("\n✅ You win this round!")
            player_score += 1
        elif winner == "ai":
            print("\n❌ Opponent wins this round!")
            ai_score += 1
        else:
            print("\n🤝 It's a tie!")
        
        print(f"\nScore: YOU {player_score} - {ai_score} OPPONENT")
    
    print("\n" + "=" * 60)
    print("🏆 FINAL RESULTS 🏆")
    print(f"YOU {player_score} - {ai_score} OPPONENT")
    
    if player_score > ai_score:
        print("\n🎉 VICTORY! You're the champion! 🎉")
    elif ai_score > player_score:
        print("\n💀 DEFEAT! Better luck next time! 💀")
    else:
        print("\n🤝 TIE! Respect to both rappers! 🤝")
    
    print("=" * 60)


if __name__ == "__main__":
    start_battle()

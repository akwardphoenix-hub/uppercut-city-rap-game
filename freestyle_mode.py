"""
Freestyle Mode - Let players rap freely with AI-generated prompts and beats.
"""

import json
import random


def load_prompts():
    """Load freestyle prompts from data file."""
    try:
        with open('data/prompts.json', 'r') as f:
            data = json.load(f)
            return data.get('freestyle_prompts', [])
    except FileNotFoundError:
        return ["rap about the city", "rap about your dreams", "rap about success"]


def load_rhymes():
    """Load rhyme suggestions from data file."""
    try:
        with open('data/rhymes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def start_freestyle():
    """Start a freestyle rap session."""
    print("🎤 FREESTYLE MODE 🎤")
    print("=" * 40)
    
    prompts = load_prompts()
    rhymes = load_rhymes()
    
    # Select a random prompt
    prompt = random.choice(prompts) if prompts else "Rap about anything!"
    print(f"\n🎯 Your prompt: {prompt}")
    
    # Show some rhyme suggestions
    if rhymes:
        rhyme_word = random.choice(list(rhymes.keys()))
        suggestions = rhymes.get(rhyme_word, [])
        print(f"\n💡 Rhyme suggestions for '{rhyme_word}': {', '.join(suggestions[:5])}")
    
    print("\n✨ Drop your bars! (Type 'quit' to exit)")
    print("-" * 40)
    
    while True:
        line = input("🎵 ")
        if line.lower() in ['quit', 'exit', 'q']:
            print("\n🔥 Great session! Keep those bars hot! 🔥")
            break
        if line.strip():
            print("   💯 Fire!")


if __name__ == "__main__":
    start_freestyle()

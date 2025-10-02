"""
Karaoke Mode - Rap along with pre-written lyrics over public domain beats.
"""

import json
import random


def load_tracks():
    """Load available karaoke tracks."""
    try:
        with open('beats/public_domain_tracks.md', 'r') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        return "# No tracks available yet!"


def load_prompts():
    """Load karaoke lyrics from data file."""
    try:
        with open('data/prompts.json', 'r') as f:
            data = json.load(f)
            return data.get('karaoke_lyrics', [])
    except FileNotFoundError:
        return ["Verse 1: Welcome to the stage / Time to turn the page"]


def start_karaoke():
    """Start a karaoke rap session."""
    print("🎤 KARAOKE MODE 🎤")
    print("=" * 40)
    
    tracks_info = load_tracks()
    lyrics = load_prompts()
    
    print("\n📀 Available Tracks:")
    print(tracks_info)
    
    # Select random lyrics
    selected_lyrics = random.choice(lyrics) if lyrics else "Rap along with the beat!"
    
    print("\n📝 Your lyrics:")
    print(selected_lyrics)
    
    print("\n🎵 Press ENTER when you're ready to start!")
    input()
    
    print("🎶 Beat playing... 🎶")
    print("\n✨ Rap along! (Type 'done' when finished)")
    print("-" * 40)
    
    while True:
        line = input("🎵 ")
        if line.lower() in ['done', 'quit', 'exit']:
            print("\n🔥 Great performance! 🔥")
            break


if __name__ == "__main__":
    start_karaoke()

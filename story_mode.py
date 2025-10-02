"""
Story Mode - Follow a narrative with branching paths based on rap choices.
"""

import json


def load_story_branches():
    """Load story branches from data file."""
    try:
        with open('data/story_branches.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "start": {
                "text": "You're backstage at the Uppercut City championship...",
                "choices": {
                    "1": {"text": "Enter the stage confidently", "next": "end"},
                    "2": {"text": "Practice more backstage", "next": "end"}
                }
            },
            "end": {
                "text": "The crowd goes wild! You're the champion!",
                "choices": {}
            }
        }


def display_scene(scene_id, story_data):
    """Display a story scene and handle choices."""
    scene = story_data.get(scene_id)
    
    if not scene:
        print("Story error: Scene not found!")
        return None
    
    print("\n" + "=" * 60)
    print(scene['text'])
    print("=" * 60)
    
    choices = scene.get('choices', {})
    
    if not choices:
        print("\n🏆 THE END 🏆")
        return None
    
    print("\nWhat do you do?")
    for key, choice in choices.items():
        print(f"  {key}. {choice['text']}")
    
    while True:
        choice = input("\n🎤 Your choice: ").strip()
        if choice in choices:
            return choices[choice]['next']
        print("Invalid choice! Try again.")


def start_story_mode():
    """Start story mode gameplay."""
    print("📖 STORY MODE 📖")
    print("=" * 60)
    print("Welcome to Uppercut City!")
    print("Your choices will determine your path to rap glory...")
    
    story_data = load_story_branches()
    current_scene = "start"
    
    while current_scene:
        current_scene = display_scene(current_scene, story_data)
    
    print("\n✨ Thanks for playing! ✨")


if __name__ == "__main__":
    start_story_mode()

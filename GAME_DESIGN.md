# Uppercut City Rap Game - Design Document

## Overview
Uppercut City Rap Game is a text-based rap battle game where players can freestyle, battle AI opponents, follow story modes, and perform karaoke-style raps over beats.

## Game Modes

### 1. Freestyle Mode (`freestyle_mode.py`)
**Purpose**: Practice rapping with AI-generated prompts and rhyme suggestions.

**Features**:
- Random prompt generation from prompts.json
- Rhyme suggestions from rhymes.json
- Open-ended practice session
- No scoring or judgment

**Flow**:
1. Load prompts and rhymes
2. Display random prompt
3. Show rhyme suggestions
4. Accept player input
5. Continue until player quits

### 2. Karaoke Mode (`karaoke_mode.py`)
**Purpose**: Rap along with pre-written lyrics over public domain beats.

**Features**:
- Pre-written lyrics to follow
- Beat selection from public_domain_tracks.md
- Guided performance

**Flow**:
1. Display available tracks
2. Show lyrics
3. Play beat (simulated)
4. Player raps along
5. Session ends when player is done

### 3. Story Mode (`story_mode.py`)
**Purpose**: Experience a narrative journey with branching paths.

**Features**:
- Branching narrative based on choices
- Multiple story paths
- Immersive storytelling
- Victory conditions

**Flow**:
1. Load story branches from story_branches.json
2. Display current scene
3. Present choices
4. Navigate to next scene based on choice
5. Continue until reaching an ending

### 4. Battle Mode (`battle_mode.py`)
**Purpose**: Compete against AI opponents in structured rap battles.

**Features**:
- Multi-round battles (best of 3)
- AI opponent responses
- Simple judging system
- Score tracking
- Battle prompts/themes

**Flow**:
1. Initialize battle (3 rounds)
2. For each round:
   - Present theme/prompt
   - Player raps
   - AI opponent responds
   - Judge the round
   - Update scores
3. Declare winner

## Data Files

### `data/prompts.json`
Contains prompts and themes for different game modes:
- `freestyle_prompts`: Topics for freestyle sessions
- `battle_prompts`: Themes for battle rounds
- `karaoke_lyrics`: Pre-written lyrics for karaoke mode

### `data/rhymes.json`
Dictionary of rhyming words organized by key words. Used to provide rhyme suggestions to players during freestyle mode.

### `data/story_branches.json`
Story structure with branching narrative paths:
- Scene descriptions
- Player choices
- Next scene references
- Story endings

### `data/cosmetics.json`
Cosmetic items for player customization (future feature):
- Chains
- Hats
- Outfits
- Accessories
- Mic styles

Each item has rarity and cost for potential progression systems.

## Beats

### `beats/public_domain_tracks.md`
Documentation of available beats:
- Beat name
- Style/genre
- Tempo (BPM)
- Description
- Source/license info

All beats must be public domain or properly licensed.

## Technical Details

### Language
- Python 3.x
- Standard library only (json, random)
- Command-line interface

### File Structure
```
uppercut-city-rap-game/
├── freestyle_mode.py
├── karaoke_mode.py
├── story_mode.py
├── battle_mode.py
├── beats/
│   └── public_domain_tracks.md
├── data/
│   ├── prompts.json
│   ├── rhymes.json
│   ├── story_branches.json
│   └── cosmetics.json
├── README.md
├── GAME_DESIGN.md
├── LICENSE
└── .gitignore
```

## Future Enhancements

### Planned Features
1. **Multiplayer Mode**: Battle against other players
2. **Progression System**: Unlock cosmetics and new content
3. **Recording**: Save and replay performances
4. **Beat Integration**: Actual audio playback
5. **Scoring System**: Advanced judging with multiple criteria
6. **Leaderboards**: Track top players
7. **Tournament Mode**: Structured competition brackets
8. **Custom Content**: Player-created prompts and stories

### Technical Improvements
1. Add actual audio playback for beats
2. Implement text-to-speech for AI responses
3. Add speech recognition for hands-free rapping
4. Create GUI version
5. Add save/load game state
6. Implement achievements system

## Design Philosophy

**Accessibility**: Text-based interface runs anywhere Python is available.

**Creativity**: Focus on player expression and creativity rather than strict rules.

**Expandability**: Modular design allows easy addition of new modes and features.

**Community**: JSON data files make it easy for community to contribute content.

## Version History

### v0.1 - Initial Prototype
- Four game modes implemented
- Basic data structure established
- Public domain beat documentation
- Core gameplay loop functional

## Credits

Created for the Uppercut City Rap Game project.
Licensed under CC0 (Public Domain).

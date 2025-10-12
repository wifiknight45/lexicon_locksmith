#!/usr/bin/env python3
"""
Enhanced Wordle Combinations Finder (Colorblind-Accessible)
Determines possible 5-letter English words based on guesses with letter placement constraints
Optimized for deutanopia (red-green colorblindness)
"""

from collections import Counter
from typing import List, Tuple
import sys
import requests

# Fetch word list from GitHub
def fetch_word_list() -> List[str]:
    """Fetch the word list from the GitHub repository."""
    url = "https://darkermango.github.io/5-Letter-words/words.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        words = response.json()
        print(f"✓ Successfully loaded {len(words)} words from remote source\n")
        return [word.lower() for word in words]
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching word list: {e}")
        print("✓ Using fallback word list\n")
        return get_fallback_word_list()

def get_fallback_word_list() -> List[str]:
    """Fallback word list in case the remote fetch fails."""
    return [
        "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
        "agent", "agree", "ahead", "alarm", "album", "alert", "align", "alike", "alive", "allow",
        "alone", "along", "alter", "amber", "amend", "among", "ample", "angel", "anger", "angle",
        "angry", "apart", "apple", "apply", "arena", "argue", "arise", "armor", "around",
        "arrow", "aside", "asset", "audio", "audit", "avoid", "awake", "award", "aware", "badly",
        "baker", "bases", "basic", "basis", "beach", "began", "begin", "being", "below", "bench",
        "billy", "birth", "black", "blade", "blame", "blank", "blast", "bleed", "bless", "blind",
        "block", "blood", "bloom", "blown", "board", "boast", "bonus", "boost", "booth", "bound",
        "brain", "brand", "brass", "brave", "bread", "break", "breed", "brief", "bring", "broad",
        "broke", "brown", "build", "built", "burst", "buyer", "cable", "calif", "candy", "carry",
        "catch", "cause", "chain", "chair", "chaos", "charm", "chart", "chase", "cheap", "check",
        "chess", "chest", "chief", "child", "china", "chose", "civil", "claim", "class", "clean",
        "clear", "click", "cliff", "climb", "clock", "close", "cloth", "cloud", "coach", "coast",
        "could", "count", "court", "cover", "crack", "craft", "crane", "crash", "crazy", "cream",
        "crime", "cross", "crowd", "crown", "crude", "curve", "cycle", "daily", "dance", "dated",
        "dealt", "death", "debut", "delay", "depth", "doing", "doubt", "dozen", "draft", "drama",
        "drank", "drawn", "dream", "dress", "dried", "drill", "drink", "drive", "drove", "dying",
        "eager", "eagle", "early", "earth", "eight", "elect", "elite", "empty", "enemy", "enjoy",
        "enter", "entry", "equal", "error", "event", "every", "exact", "exist", "extra", "faith",
        "false", "fault", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed",
        "flash", "fleet", "flesh", "flight", "floor", "fluid", "focus", "force", "forth", "forty",
        "forum", "found", "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny",
        "giant", "given", "glass", "globe", "glory", "going", "grace", "grade", "grain", "grand",
        "grant", "graph", "grasp", "grass", "grave", "great", "green", "greet", "grief", "gross",
        "group", "grown", "guard", "guess", "guest", "guide", "guild", "guilt", "happy", "harry",
        "harsh", "haste", "heart", "heavy", "hence", "henry", "horse", "hotel", "house", "human",
        "ideal", "image", "imply", "index", "inner", "input", "issue", "japan", "jimmy", "jones",
        "judge", "known", "label", "large", "laser", "later", "laugh", "layer", "learn", "lease",
        "least", "leave", "legal", "lemon", "level", "lewis", "light", "limit", "links", "lives",
        "local", "logic", "loose", "lower", "lucky", "lunch", "lying", "magic", "major", "maker",
        "march", "maria", "match", "maybe", "mayor", "meant", "media", "metal", "might", "minor",
        "minus", "mixed", "model", "money", "month", "moral", "motor", "mount", "mouse", "mouth",
        "movie", "music", "needs", "never", "newly", "night", "noise", "north", "noted", "novel",
        "nurse", "occur", "ocean", "offer", "often", "order", "other", "ought", "outer", "owned",
        "owner", "paint", "panel", "panic", "paper", "party", "peace", "peter", "phase", "phone",
        "photo", "piece", "pilot", "pitch", "place", "plain", "plane", "plant", "plate", "plaza",
        "point", "poker", "polar", "pound", "power", "press", "price", "pride", "prime", "print",
        "prior", "prize", "proof", "proud", "prove", "queen", "query", "quest", "queue", "quick",
        "quiet", "quite", "radio", "raise", "range", "rapid", "ratio", "reach", "ready", "refer",
        "reign", "relax", "reply", "rider", "ridge", "rifle", "right", "rigid", "risky", "rival",
        "river", "robin", "rocky", "roman", "rough", "round", "route", "royal", "rural", "scale",
        "scene", "scope", "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp",
        "sheet", "shelf", "shell", "shift", "shine", "shirt", "shock", "shoot", "shore", "short",
        "shown", "sight", "since", "sixth", "sixty", "sized", "skill", "sleep", "slide", "small",
        "smart", "smile", "smith", "smoke", "solid", "solve", "sorry", "sound", "south", "space",
        "spare", "speak", "speed", "spend", "spent", "split", "spoke", "sport", "staff", "stage",
        "stake", "stand", "start", "state", "steam", "steel", "steep", "steer", "steve", "stick",
        "still", "stock", "stone", "stood", "store", "storm", "story", "strip", "stuck", "study",
        "stuff", "style", "sugar", "suite", "sunny", "super", "surge", "sweet", "swift", "swing",
        "sword", "table", "taken", "taste", "taxes", "teach", "terry", "texas", "thank", "theft",
        "their", "theme", "there", "these", "thick", "thing", "think", "third", "those", "three",
        "threw", "throw", "thumb", "tiger", "tight", "timer", "title", "today", "topic", "total",
        "touch", "tough", "tower", "track", "trade", "trail", "train", "trait", "treat", "trend",
        "trial", "tribe", "trick", "tried", "troop", "truck", "truly", "trump", "trust", "truth",
        "twice", "uncle", "under", "undue", "union", "unity", "until", "upper", "upset", "urban",
        "usage", "usual", "valid", "value", "video", "virus", "visit", "vital", "vocal", "voice",
        "waste", "watch", "water", "wheel", "where", "which", "while", "white", "whole", "whose",
        "woman", "women", "world", "worry", "worse", "worst", "worth", "would", "wound", "write",
        "wrong", "wrote", "yield", "young", "yours", "youth", "zones"
    ]

# Color schemes - Deutanopia-friendly
STANDARD_COLORS = {
    'correct': '\033[94m',      # Blue (replaces green)
    'present': '\033[95m',      # Magenta (replaces yellow)
    'absent': '\033[90m',       # Gray (replaces red)
    'reset': '\033[0m',
    'bold': '\033[1m',
    'info': '\033[96m',         # Cyan for info
    'success': '\033[94m',      # Blue
    'error': '\033[91m',        # Red (only for errors, not game feedback)
    'warning': '\033[93m'       # Yellow for warnings
}

HIGH_CONTRAST_COLORS = {
    'correct': '\033[97;44m',   # White on blue
    'present': '\033[30;105m',  # Black on magenta
    'absent': '\033[97;40m',    # White on black
    'reset': '\033[0m',
    'bold': '\033[1;97m',       # Bold white
    'info': '\033[97;46m',      # White on cyan
    'success': '\033[30;106m',  # Black on cyan
    'error': '\033[97;41m',     # White on red
    'warning': '\033[30;103m'   # Black on yellow
}

# Symbols for additional distinction
SYMBOLS = {
    'correct': '█',   # Solid block
    'present': '○',   # Circle
    'absent': '·'     # Dot
}

# Global setting for color mode
USE_HIGH_CONTRAST = False
USE_SYMBOLS = True


def get_color(key: str) -> str:
    """Get color code based on current mode."""
    colors = HIGH_CONTRAST_COLORS if USE_HIGH_CONTRAST else STANDARD_COLORS
    return colors.get(key, '')


def format_feedback_display(guess: str, feedback: str) -> str:
    """Format guess with colorblind-friendly colors and symbols."""
    output = []
    feedback_map = {'G': 'correct', 'Y': 'present', 'R': 'absent'}
    
    for letter, fb in zip(guess.upper(), feedback.upper()):
        status = feedback_map.get(fb, 'absent')
        color = get_color(status)
        reset = get_color('reset')
        symbol = SYMBOLS[status] if USE_SYMBOLS else ''
        
        output.append(f"{color}{symbol}{letter}{reset}")
    
    return ' '.join(output)


def print_legend():
    """Print color legend for reference."""
    print(f"\n{get_color('bold')}Legend:{get_color('reset')}")
    print(f"  {get_color('correct')}{SYMBOLS['correct'] if USE_SYMBOLS else ''}█{get_color('reset')} Blue/Solid = Correct position")
    print(f"  {get_color('present')}{SYMBOLS['present'] if USE_SYMBOLS else ''}○{get_color('reset')} Magenta/Circle = Wrong position")
    print(f"  {get_color('absent')}{SYMBOLS['absent'] if USE_SYMBOLS else ''}·{get_color('reset')} Gray/Dot = Not in word\n")


def validate_guess(guess: str, feedback: str) -> Tuple[bool, str]:
    """Validate that the guess and feedback are correctly formatted."""
    if len(guess) != 5 or not guess.isalpha():
        return False, "Guess must be a 5-letter word containing only letters."
    if len(feedback) != 5 or not all(c in 'GYR' for c in feedback.upper()):
        return False, "Feedback must be 5 characters, each 'G' (correct), 'Y' (present), or 'R' (absent)."
    return True, ""


def is_valid_word(word: str, guess: str, feedback: str) -> bool:
    """
    Check if a word is valid given a guess and its feedback.
    
    Rules:
    - Correct (G): Letter is in the correct position
    - Present (Y): Letter exists in the word but wrong position
    - Absent (R): Letter doesn't exist in the word (or no more instances exist)
    """
    guess = guess.lower()
    word = word.lower()
    feedback = feedback.upper()
    
    # Count occurrences of each letter in guess by feedback type
    green_positions = {}
    yellow_letters = Counter()
    red_letters = set()
    
    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb == 'G':
            green_positions[i] = letter
            yellow_letters[letter] += 1
        elif fb == 'Y':
            yellow_letters[letter] += 1
        elif fb == 'R':
            red_letters.add(letter)
    
    # Check green constraints (correct position)
    for pos, letter in green_positions.items():
        if word[pos] != letter:
            return False
    
    # Check yellow constraints (letter exists but wrong position)
    word_counter = Counter(word)
    for letter, min_count in yellow_letters.items():
        if word_counter[letter] < min_count:
            return False
    
    # Check that yellow letters aren't in their guessed positions
    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb == 'Y' and word[i] == letter:
            return False
    
    # Check red constraints (letter shouldn't appear more than green/yellow count)
    for letter in red_letters:
        required_count = yellow_letters.get(letter, 0)
        if word_counter[letter] > required_count:
            return False
    
    return True


def filter_words(guesses: List[str], feedbacks: List[str], word_list: List[str]) -> List[str]:
    """Filter word list based on guesses and their feedbacks."""
    possible_words = word_list.copy()
    
    for guess, feedback in zip(guesses, feedbacks):
        possible_words = [
            word for word in possible_words 
            if is_valid_word(word, guess, feedback)
        ]
    
    return possible_words


def suggest_next_guess(possible_words: List[str]) -> List[str]:
    """Suggest good next guesses based on letter frequency."""
    if len(possible_words) <= 5:
        return possible_words
    
    # Count letter frequency across all positions
    letter_freq = Counter()
    for word in possible_words:
        letter_freq.update(set(word))  # Count each letter once per word
    
    # Score words by unique letter frequency
    word_scores = []
    for word in possible_words:
        score = sum(letter_freq[letter] for letter in set(word))
        word_scores.append((score, word))
    
    # Return top 5 suggestions
    word_scores.sort(reverse=True)
    return [word for _, word in word_scores[:5]]


def configure_accessibility():
    """Configure accessibility settings at startup."""
    global USE_HIGH_CONTRAST, USE_SYMBOLS
    
    print(f"{get_color('bold')}Accessibility Settings{get_color('reset')}")
    print("This tool is optimized for deutanopia (red-green colorblindness)")
    print("\nOptions:")
    print("  1. Standard mode (blue/magenta/gray with symbols)")
    print("  2. High contrast mode (enhanced backgrounds with symbols)")
    print("  3. No symbols (colors only)")
    
    try:
        choice = input("\nSelect mode (1/2/3) [default: 1]: ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = '1'
    
    if choice == '2':
        USE_HIGH_CONTRAST = True
        USE_SYMBOLS = True
    elif choice == '3':
        USE_HIGH_CONTRAST = False
        USE_SYMBOLS = False
    else:
        USE_HIGH_CONTRAST = False
        USE_SYMBOLS = True
    
    print(f"\n{get_color('success')}✓ Mode configured{get_color('reset')}\n")


def main():
    """Main function to run the Wordle finder."""
    print("=" * 70)
    print(f"{get_color('bold')}Enhanced Wordle Combinations Finder (Colorblind-Accessible){get_color('reset')}")
    print("=" * 70)
    
    # Configure accessibility
    configure_accessibility()
    
    # Fetch word list
    WORD_LIST = fetch_word_list()
    
    # Show legend
    print_legend()
    
    print(f"{get_color('bold')}Instructions:{get_color('reset')}")
    print("  - Enter your guess (5-letter word)")
    print("  - Enter feedback using: G (correct position), Y (wrong position), R (not in word)")
    print("  - Type 'done' when finished entering guesses")
    print("  - Type 'quit' to exit")
    print("  - Type 'legend' to see the color guide again\n")
    print(f"{get_color('info')}Example:{get_color('reset')}")
    print("  Guess: crane")
    print("  Feedback: GYRRR")
    print(f"  Display: {format_feedback_display('crane', 'GYRRR')}")
    print("  (C is correct position, R is wrong position, A/N/E not in word)\n")
    
    guesses = []
    feedbacks = []
    
    while True:
        try:
            guess_input = input(f"{get_color('bold')}Enter guess{get_color('reset')} (or 'done'/'quit'/'legend'): ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{get_color('warning')}Exiting...{get_color('reset')}")
            break
        
        if guess_input in ['quit', 'exit', 'q']:
            print(f"{get_color('info')}Goodbye!{get_color('reset')}")
            break
        
        if guess_input == 'legend':
            print_legend()
            continue
        
        if guess_input == 'done':
            break
        
        try:
            feedback_input = input(f"{get_color('bold')}Enter feedback{get_color('reset')} (G/Y/R): ").upper().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{get_color('warning')}Exiting...{get_color('reset')}")
            break
        
        valid, error = validate_guess(guess_input, feedback_input)
        if not valid:
            print(f"{get_color('error')}✗ Error: {error}{get_color('reset')}\n")
            continue
        
        guesses.append(guess_input)
        feedbacks.append(feedback_input)
        
        # Show visual representation
        print(f"  Visual: {format_feedback_display(guess_input, feedback_input)}")
        
        # Show intermediate results
        possible_words = filter_words(guesses, feedbacks, WORD_LIST)
        print(f"{get_color('success')}✓ Added guess. Remaining possibilities: {len(possible_words)}{get_color('reset')}\n")
    
    if not guesses:
        print(f"\n{get_color('info')}📊 No guesses provided. Total words in dictionary: {len(WORD_LIST)}{get_color('reset')}")
        return
    
    # Filter possible words
    possible_words = filter_words(guesses, feedbacks, WORD_LIST)
    
    # Output results
    print("\n" + "=" * 70)
    print(f"{get_color('bold')}RESULTS{get_color('reset')}")
    print("=" * 70)
    
    # Show all guesses
    print(f"\n{get_color('bold')}Your guesses:{get_color('reset')}")
    for i, (guess, feedback) in enumerate(zip(guesses, feedbacks), 1):
        print(f"  {i}. {format_feedback_display(guess, feedback)}")
    
    if possible_words:
        print(f"\n{get_color('success')}✓ Found {len(possible_words)} possible word(s):{get_color('reset')}\n")
        
        # Sort and display
        for i, word in enumerate(sorted(possible_words), 1):
            print(f"  {i:2d}. {get_color('bold')}{word.upper()}{get_color('reset')}")
        
        # Show suggestions if there are many possibilities
        if len(possible_words) > 5:
            print(f"\n{get_color('info')}💡 Suggested next guesses (best letter coverage):{get_color('reset')}")
            suggestions = suggest_next_guess(possible_words)
            for word in suggestions:
                print(f"  → {get_color('bold')}{word.upper()}{get_color('reset')}")
    else:
        print(f"\n{get_color('error')}✗ No words match the given constraints.{get_color('reset')}")
        print(f"   {get_color('warning')}Check your feedback entries for errors.{get_color('reset')}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

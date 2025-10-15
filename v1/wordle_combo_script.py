#!/usr/bin/env python3
"""
Enhanced Wordle Combinations Finder
Determines possible 5-letter English words based on guesses with letter placement constraints
"""

from collections import Counter
from typing import List, Tuple

# Comprehensive list of common 5-letter English words
WORD_LIST = [
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
    "agent", "agree", "ahead", "alarm", "album", "alert", "align", "alike", "alive", "allow",
    "alone", "along", "alter", "amber", "amend", "among", "ample", "angel", "anger", "angle",
    "angry", "apart", "apple", "apply", "arena", "argue", "arise", "armor", "army", "around",
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


def validate_guess(guess: str, feedback: str) -> Tuple[bool, str]:
    """Validate that the guess and feedback are correctly formatted."""
    if len(guess) != 5 or not guess.isalpha():
        return False, "Guess must be a 5-letter word containing only letters."
    if len(feedback) != 5 or not all(c in 'GYR' for c in feedback.upper()):
        return False, "Feedback must be 5 characters, each 'G' (green), 'Y' (yellow), or 'R' (red)."
    return True, ""


def is_valid_word(word: str, guess: str, feedback: str) -> bool:
    """
    Check if a word is valid given a guess and its feedback.
    
    Rules:
    - Green (G): Letter is in the correct position
    - Yellow (Y): Letter exists in the word but wrong position
    - Red (R): Letter doesn't exist in the word (or no more instances exist)
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


def main():
    """Main function to run the Wordle finder."""
    print("=" * 60)
    print("Enhanced Wordle Combinations Finder")
    print("=" * 60)
    print("\nInstructions:")
    print("  - Enter your guess (5-letter word)")
    print("  - Enter feedback: G (green), Y (yellow), R (red)")
    print("  - Type 'done' when finished entering guesses")
    print("  - Type 'quit' to exit\n")
    print("Example:")
    print("  Guess: crane")
    print("  Feedback: GYRRR (C is green, R is yellow, rest are red)\n")
    
    guesses = []
    feedbacks = []
    
    while True:
        try:
            guess_input = input("Enter guess (or 'done'/'quit'): ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting...")
            break
        
        if guess_input in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if guess_input == 'done':
            break
        
        try:
            feedback_input = input("Enter feedback (G/Y/R): ").upper().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting...")
            break
        
        valid, error = validate_guess(guess_input, feedback_input)
        if not valid:
            print(f"❌ Error: {error}\n")
            continue
        
        guesses.append(guess_input)
        feedbacks.append(feedback_input)
        
        # Show intermediate results
        possible_words = filter_words(guesses, feedbacks, WORD_LIST)
        print(f"✓ Added guess. Remaining possibilities: {len(possible_words)}\n")
    
    if not guesses:
        print(f"\n📊 No guesses provided. Total words in dictionary: {len(WORD_LIST)}")
        return
    
    # Filter possible words
    possible_words = filter_words(guesses, feedbacks, WORD_LIST)
    
    # Output results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if possible_words:
        print(f"\n✓ Found {len(possible_words)} possible word(s):\n")
        
        # Sort and display
        for i, word in enumerate(sorted(possible_words), 1):
            print(f"  {i:2d}. {word.upper()}")
        
        # Show suggestions if there are many possibilities
        if len(possible_words) > 5:
            print(f"\n💡 Suggested next guesses (best letter coverage):")
            suggestions = suggest_next_guess(possible_words)
            for word in suggestions:
                print(f"  → {word.upper()}")
    else:
        print("\n❌ No words match the given constraints.")
        print("   Check your feedback entries for errors.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

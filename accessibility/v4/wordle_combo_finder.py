#!/usr/bin/env python3
"""
Enhanced Wordle Combinations Finder (Colorblind-Accessible)
Determines possible 5-letter English words based on guesses with letter placement constraints
Optimized for deutanopia (red-green colorblindness)
"""

from collections import Counter
from typing import List, Tuple
import sys

def get_word_list() -> List[str]:
    """Complete word list for Wordle solving."""
    # [WORD LIST RETAINED FROM ORIGINAL - Not repeated here for brevity]
    return [
        "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
        # ... (full word list as in original)
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

# Global settings
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
    
    Enhanced version with proper handling of duplicate letters.
    """
    guess = guess.lower()
    word = word.lower()
    feedback = feedback.upper()
    
    # First pass: identify all constraints
    green_positions = {}  # position -> letter
    yellow_info = []      # (position, letter) pairs
    
    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb == 'G':
            green_positions[i] = letter
        elif fb == 'Y':
            yellow_info.append((i, letter))
    
    # Calculate minimum required count for each letter
    min_counts = Counter()
    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb in ['G', 'Y']:
            min_counts[letter] += 1
    
    # Calculate maximum allowed count (when R appears)
    max_counts = {}
    for letter in set(guess):
        letter_feedbacks = [fb for l, fb in zip(guess, feedback) if l == letter]
        if 'R' in letter_feedbacks:
            # Count only G and Y for this letter
            max_counts[letter] = sum(1 for fb in letter_feedbacks if fb in ['G', 'Y'])
    
    # Check green constraints
    for pos, letter in green_positions.items():
        if word[pos] != letter:
            return False
    
    # Check yellow constraints
    for pos, letter in yellow_info:
        if word[pos] == letter:  # Can't be in the same position
            return False
    
    # Check letter counts
    word_counts = Counter(word)
    for letter, min_count in min_counts.items():
        if word_counts[letter] < min_count:
            return False
    
    for letter, max_count in max_counts.items():
        if word_counts[letter] > max_count:
            return False
    
    # Check letters marked as absent (with no G or Y)
    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb == 'R' and letter not in min_counts:
            if letter in word:
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


def display_known_pattern(guesses: List[str], feedbacks: List[str]):
    """Display the known letter pattern."""
    known = ['_'] * 5
    wrong_positions = {i: set() for i in range(5)}
    must_contain = set()
    cannot_contain = set()
    
    for guess, feedback in zip(guesses, feedbacks):
        for i, (letter, fb) in enumerate(zip(guess.lower(), feedback.upper())):
            if fb == 'G':
                known[i] = letter.upper()
            elif fb == 'Y':
                must_contain.add(letter.upper())
                wrong_positions[i].add(letter.upper())
            elif fb == 'R':
                # Only add to cannot_contain if letter has no G or Y elsewhere
                if not any(f in ['G', 'Y'] for l, f in zip(guess, feedback) if l == letter):
                    cannot_contain.add(letter.upper())
    
    pattern = ' '.join(known)
    print(f"\n{get_color('bold')}Known Pattern:{get_color('reset')} {pattern}")
    
    if must_contain:
        print(f"{get_color('present')}Must contain:{get_color('reset')} {', '.join(sorted(must_contain))}")
    
    if cannot_contain:
        print(f"{get_color('absent')}Cannot contain:{get_color('reset')} {', '.join(sorted(cannot_contain))}")


def display_possible_words(possible_words: List[str], max_display: int = 20):
    """Display the list of possible words after filtering."""
    num_words = len(possible_words)
    
    if num_words == 0:
        print(f"\n{get_color('error')}✗ No possible words remain!{get_color('reset')}")
        print(f"   {get_color('warning')}Check your feedback entries for errors.{get_color('reset')}")
        return
    
    if num_words == 1:
        print(f"\n{get_color('success')}🎉 Found the answer: {get_color('bold')}{possible_words[0].upper()}{get_color('reset')}")
        return
    
    print(f"\n{get_color('info')}📋 Possible words ({num_words}):{get_color('reset')}")
    
    # Sort alphabetically for consistent display
    sorted_words = sorted(possible_words)
    
    if num_words <= max_display:
        # Display all words in columns
        cols = 4
        for i in range(0, len(sorted_words), cols):
            row_words = sorted_words[i:i+cols]
            formatted = [f"{word.upper():6s}" for word in row_words]
            print(f"  {' '.join(formatted)}")
    else:
        # Display first max_display words, then show count
        for i in range(0, min(max_display, len(sorted_words)), 4):
            row_words = sorted_words[i:i+4]
            formatted = [f"{word.upper():6s}" for word in row_words]
            print(f"  {' '.join(formatted)}")
        
        remaining = num_words - max_display
        if remaining > 0:
            print(f"  {get_color('info')}... and {remaining} more{get_color('reset')}")


def suggest_next_guess(possible_words: List[str], all_words: List[str]) -> List[str]:
    """Suggest good next guesses using letter frequency analysis."""
    if len(possible_words) <= 2:
        return possible_words
    
    # If many possibilities remain, consider all words for maximum information gain
    if len(possible_words) > 20:
        search_space = all_words[:2000]  # Limit for performance
    else:
        search_space = possible_words
    
    # Score by positional letter frequency
    position_freq = [Counter() for _ in range(5)]
    for word in possible_words:
        for i, letter in enumerate(word):
            position_freq[i][letter] += 1
    
    word_scores = []
    for word in search_space:
        unique_letters = len(set(word))
        position_score = sum(
            position_freq[i][letter] 
            for i, letter in enumerate(word)
        )
        # Prefer words with unique letters for more information
        score = position_score * (unique_letters / 5)
        word_scores.append((score, word))
    
    word_scores.sort(reverse=True)
    return [word for _, word in word_scores[:5]]


def show_statistics(possible_words: List[str]):
    """Show helpful statistics about remaining words."""
    if not possible_words:
        return
    
    # Letter frequency
    letter_freq = Counter()
    for word in possible_words:
        letter_freq.update(word)
    
    print(f"\n{get_color('info')}📊 Statistics:{get_color('reset')}")
    print(f"  Most common letters: {', '.join(l.upper() for l, _ in letter_freq.most_common(5))}")
    
    # First letter distribution
    first_letters = Counter(w[0] for w in possible_words)
    print(f"  Most common first letters: {', '.join(l.upper() for l, _ in first_letters.most_common(3))}")


def export_results(guesses: List[str], feedbacks: List[str], possible_words: List[str], filename: str = "wordle_results.txt"):
    """Export results to a file."""
    try:
        with open(filename, 'w') as f:
            f.write("Wordle Solver Results\n")
            f.write("=" * 50 + "\n\n")
            f.write("Guesses:\n")
            for guess, feedback in zip(guesses, feedbacks):
                f.write(f"  {guess.upper()} -> {feedback}\n")
            f.write(f"\nPossible words ({len(possible_words)}):\n")
            for word in sorted(possible_words):
                f.write(f"  {word.upper()}\n")
        print(f"\n{get_color('success')}✓ Results exported to {filename}{get_color('reset')}")
    except Exception as e:
        print(f"\n{get_color('error')}✗ Error exporting results: {e}{get_color('reset')}")


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
    
    # Get word list
    WORD_LIST = get_word_list()
    WORD_SET = set(WORD_LIST)  # For O(1) lookups
    
    print(f"{get_color('success')}✓ Loaded {len(WORD_LIST)} words{get_color('reset')}")
    
    # Show legend
    print_legend()
    
    print(f"{get_color('bold')}Instructions:{get_color('reset')}")
    print("  - Enter your guess (5-letter word)")
    print("  - Enter feedback using: G (correct position), Y (wrong position), R (not in word)")
    print("  - Type 'done' when finished entering guesses")
    print("  - Type 'undo' to remove the last guess")
    print("  - Type 'export' to save results to a file")
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
            guess_input = input(f"{get_color('bold')}Enter guess{get_color('reset')} (or 'done'/'quit'/'undo'/'export'/'legend'): ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{get_color('warning')}Exiting...{get_color('reset')}")
            break
        
        if guess_input in ['quit', 'exit', 'q']:
            print(f"{get_color('info')}Goodbye!{get_color('reset')}")
            break
        
        if guess_input == 'legend':
            print_legend()
            continue
        
        if guess_input == 'undo':
            if guesses:
                removed_guess = guesses.pop()
                feedbacks.pop()
                print(f"{get_color('success')}✓ Removed guess: {removed_guess}{get_color('reset')}\n")
                
                # Show updated results after undo
                if guesses:
                    possible_words = filter_words(guesses, feedbacks, WORD_LIST)
                    display_known_pattern(guesses, feedbacks)
                    display_possible_words(possible_words)
                    
                    if len(possible_words) > 5:
                        show_statistics(possible_words)
                        print(f"\n{get_color('info')}💡 Suggested next guesses:{get_color('reset')}")
                        suggestions = suggest_next_guess(possible_words, WORD_LIST)
                        for word in suggestions:
                            print(f"  → {get_color('bold')}{word.upper()}{get_color('reset')}")
                else:
                    print(f"{get_color('info')}No guesses remaining. Starting fresh!{get_color('reset')}\n")
            else:
                print(f"{get_color('warning')}No guesses to undo{get_color('reset')}\n")
            continue
        
        if guess_input == 'export':
            if guesses:
                possible_words = filter_words(guesses, feedbacks, WORD_LIST)
                export_results(guesses, feedbacks, possible_words)
            else:
                print(f"{get_color('warning')}No guesses to export{get_color('reset')}\n")
            continue
        
        if guess_input == 'done':
            break
        
        # Validate word is in dictionary
        if guess_input not in WORD_SET:
            print(f"{get_color('warning')}⚠ '{guess_input}' not in dictionary. Continue anyway? (y/n): {get_color('reset')}", end='')
            try:
                if input().lower().strip() != 'y':
                    continue
            except (EOFError, KeyboardInterrupt):
                print()
                continue
        
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
        
        # Filter and display possible words immediately after each guess
        possible_words = filter_words(guesses, feedbacks, WORD_LIST)
        
        # Show pattern
        display_known_pattern(guesses, feedbacks)
        
        # Display possible words list
        display_possible_words(possible_words)
        
        # Show statistics and suggestions if multiple possibilities remain
        if len(possible_words) > 1:
            if len(possible_words) > 5:
                show_statistics(possible_words)
            
            if len(possible_words) > 5:
                print(f"\n{get_color('info')}💡 Suggested next guesses (best letter coverage):{get_color('reset')}")
                suggestions = suggest_next_guess(possible_words, WORD_LIST)
                for word in suggestions:
                    print(f"  → {get_color('bold')}{word.upper()}{get_color('reset')}")
        
        print()  # Extra line for readability
    
    if not guesses:
        print(f"\n{get_color('info')}📊 No guesses provided. Total words in dictionary: {len(WORD_LIST)}{get_color('reset')}")
        return
    
    # Filter possible words for final results
    possible_words = filter_words(guesses, feedbacks, WORD_LIST)
    
    # Output final results summary
    print("\n" + "=" * 70)
    print(f"{get_color('bold')}FINAL RESULTS{get_color('reset')}")
    print("=" * 70)
    
    # Show all guesses
    print(f"\n{get_color('bold')}Your guesses:{get_color('reset')}")
    for i, (guess, feedback) in enumerate(zip(guesses, feedbacks), 1):
        print(f"  {i}. {format_feedback_display(guess, feedback)}")
    
    # Show final pattern
    display_known_pattern(guesses, feedbacks)
    
    # Display final possible words
    display_possible_words(possible_words, max_display=50)
    
    if len(possible_words) > 1:
        show_statistics(possible_words)
    
    print("\n" + "=" * 70)
    
    # Offer to export
    if possible_words and len(possible_words) > 1:
        try:
            export_choice = input(f"\n{get_color('info')}Export results to file? (y/n): {get_color('reset')}").lower().strip()
            if export_choice == 'y':
                export_results(guesses, feedbacks, possible_words)
        except (EOFError, KeyboardInterrupt):
            print()


if __name__ == "__main__":
    main()

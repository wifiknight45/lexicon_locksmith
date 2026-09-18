#!/usr/bin/env python3
"""
Enhanced Wordle Combinations Finder (Colorblind-Accessible)

Canonical solver promoted from accessibility/v5 (ranking + accessibility modes).
Loads words from wordlist.txt at the repository root (one lowercase 5-letter
word per line).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import List, Optional, Tuple, Union

# Repo root = parent of this package directory
_PACKAGE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PACKAGE_DIR.parent
DEFAULT_WORDLIST_PATH = _REPO_ROOT / "wordlist.txt"


def load_word_list(path: Optional[Union[Path, str]] = None) -> List[str]:
    """
    Load sanitized word list from disk.

    Expects one lowercase 5-letter alphabetic word per line.
    Non-conforming lines are skipped; results are deduplicated and sorted.
    """
    wordlist_path = Path(path) if path is not None else DEFAULT_WORDLIST_PATH
    if not wordlist_path.is_file():
        raise FileNotFoundError(
            f"Word list not found: {wordlist_path}\n"
            "Expected wordlist.txt at the repository root "
            "(one lowercase 5-letter word per line)."
        )

    words = set()  # type: set
    with wordlist_path.open(encoding="utf-8") as handle:
        for line in handle:
            word = line.strip().lower()
            if len(word) == 5 and word.isalpha():
                words.add(word)

    if not words:
        raise ValueError(f"No valid 5-letter words found in {wordlist_path}")

    return sorted(words)


# Color schemes — deutanopia-friendly
STANDARD_COLORS = {
    "correct": "\033[94m",  # Blue (replaces green)
    "present": "\033[95m",  # Magenta (replaces yellow)
    "absent": "\033[90m",  # Gray (replaces red)
    "reset": "\033[0m",
    "bold": "\033[1m",
    "info": "\033[96m",
    "success": "\033[94m",
    "error": "\033[91m",
    "warning": "\033[93m",
}

HIGH_CONTRAST_COLORS = {
    "correct": "\033[97;44m",
    "present": "\033[30;105m",
    "absent": "\033[97;40m",
    "reset": "\033[0m",
    "bold": "\033[1;97m",
    "info": "\033[97;46m",
    "success": "\033[30;106m",
    "error": "\033[97;41m",
    "warning": "\033[30;103m",
}

SYMBOLS = {
    "correct": "█",
    "present": "○",
    "absent": "·",
}

USE_HIGH_CONTRAST = False
USE_SYMBOLS = True


def get_color(key: str) -> str:
    """Get color code based on current mode."""
    colors = HIGH_CONTRAST_COLORS if USE_HIGH_CONTRAST else STANDARD_COLORS
    return colors.get(key, "")


def format_feedback_display(guess: str, feedback: str) -> str:
    """Format guess with colorblind-friendly colors and symbols."""
    output = []
    feedback_map = {"G": "correct", "Y": "present", "R": "absent"}

    for letter, fb in zip(guess.upper(), feedback.upper()):
        status = feedback_map.get(fb, "absent")
        color = get_color(status)
        reset = get_color("reset")
        symbol = SYMBOLS[status] if USE_SYMBOLS else ""
        output.append(f"{color}{symbol}{letter}{reset}")

    return " ".join(output)


def print_legend() -> None:
    """Print color legend for reference."""
    print(f"\n{get_color('bold')}Legend:{get_color('reset')}")
    print(
        f"  {get_color('correct')}{SYMBOLS['correct'] if USE_SYMBOLS else ''}"
        f"{get_color('reset')} Blue/Solid = Correct position"
    )
    print(
        f"  {get_color('present')}{SYMBOLS['present'] if USE_SYMBOLS else ''}"
        f"{get_color('reset')} Magenta/Circle = Wrong position"
    )
    print(
        f"  {get_color('absent')}{SYMBOLS['absent'] if USE_SYMBOLS else ''}"
        f"{get_color('reset')} Gray/Dot = Not in word\n"
    )


def validate_guess(guess: str, feedback: str) -> Tuple[bool, str]:
    """Validate that the guess and feedback are correctly formatted."""
    if len(guess) != 5 or not guess.isalpha():
        return False, "Guess must be a 5-letter word containing only letters."
    if len(feedback) != 5 or not all(c in "GYR" for c in feedback.upper()):
        return (
            False,
            "Feedback must be 5 characters, each 'G' (correct), "
            "'Y' (present), or 'R' (absent).",
        )
    return True, ""


def is_valid_word(word: str, guess: str, feedback: str) -> bool:
    """
    Check if a word is valid given a guess and its feedback.

    Handles duplicate letters via min/max letter counts from G/Y/R feedback.
    """
    guess = guess.lower()
    word = word.lower()
    feedback = feedback.upper()

    green_positions = {}
    yellow_info = []

    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb == "G":
            green_positions[i] = letter
        elif fb == "Y":
            yellow_info.append((i, letter))

    min_counts = Counter()
    for letter, fb in zip(guess, feedback):
        if fb in ("G", "Y"):
            min_counts[letter] += 1

    max_counts = {}
    for letter in set(guess):
        letter_feedbacks = [fb for l, fb in zip(guess, feedback) if l == letter]
        if "R" in letter_feedbacks:
            max_counts[letter] = sum(1 for fb in letter_feedbacks if fb in ("G", "Y"))

    for pos, letter in green_positions.items():
        if word[pos] != letter:
            return False

    for pos, letter in yellow_info:
        if word[pos] == letter:
            return False

    word_counts = Counter(word)
    for letter, min_count in min_counts.items():
        if word_counts[letter] < min_count:
            return False

    for letter, max_count in max_counts.items():
        if word_counts[letter] > max_count:
            return False

    for letter, fb in zip(guess, feedback):
        if fb == "R" and letter not in min_counts:
            if letter in word:
                return False

    return True


def filter_words(
    guesses: List[str], feedbacks: List[str], word_list: List[str]
) -> List[str]:
    """Filter word list based on guesses and their feedbacks."""
    possible_words = list(word_list)

    for guess, feedback in zip(guesses, feedbacks):
        possible_words = [
            word
            for word in possible_words
            if is_valid_word(word, guess, feedback)
        ]

    return possible_words


def display_known_pattern(guesses: List[str], feedbacks: List[str]) -> None:
    """Display the known letter pattern."""
    known = ["_"] * 5
    must_contain = set()  # type: set
    cannot_contain = set()  # type: set

    for guess, feedback in zip(guesses, feedbacks):
        for i, (letter, fb) in enumerate(zip(guess.lower(), feedback.upper())):
            if fb == "G":
                known[i] = letter.upper()
            elif fb == "Y":
                must_contain.add(letter.upper())
            elif fb == "R":
                if not any(
                    f in ("G", "Y") for l, f in zip(guess, feedback) if l == letter
                ):
                    cannot_contain.add(letter.upper())

    pattern = " ".join(known)
    print(f"\n{get_color('bold')}Known Pattern:{get_color('reset')} {pattern}")

    if must_contain:
        print(
            f"{get_color('present')}Must contain:{get_color('reset')} "
            f"{', '.join(sorted(must_contain))}"
        )

    if cannot_contain:
        print(
            f"{get_color('absent')}Cannot contain:{get_color('reset')} "
            f"{', '.join(sorted(cannot_contain))}"
        )


def rank_words_by_relevance(
    words: List[str], all_possible_words: List[str]
) -> List[str]:
    """
    Rank words by relevance using positional and overall letter frequency.

    Returns words sorted from most to least likely.
    """
    if len(words) <= 1:
        return list(words)

    position_freq = [Counter() for _ in range(5)]
    for word in all_possible_words:
        for i, letter in enumerate(word):
            position_freq[i][letter] += 1

    overall_freq = Counter()
    for word in all_possible_words:
        overall_freq.update(set(word))

    index_lookup = {word: idx for idx, word in enumerate(words)}
    word_scores = []
    for word in words:
        position_score = sum(position_freq[i][letter] for i, letter in enumerate(word))
        letter_score = sum(overall_freq[letter] for letter in set(word))
        commonality_bonus = 1000 - index_lookup.get(word, 0)
        unique_bonus = len(set(word)) * 10
        total_score = (
            (position_score * 2) + letter_score + (commonality_bonus * 0.1) + unique_bonus
        )
        word_scores.append((total_score, word))

    word_scores.sort(reverse=True)
    return [word for _, word in word_scores]


def suggest_next_guess(possible_words: List[str], all_words: List[str]) -> List[str]:
    """Suggest good next guesses using letter frequency analysis."""
    if len(possible_words) <= 2:
        return list(possible_words)

    if len(possible_words) > 20:
        search_space = all_words[:2000]
    else:
        search_space = possible_words

    position_freq = [Counter() for _ in range(5)]
    for word in possible_words:
        for i, letter in enumerate(word):
            position_freq[i][letter] += 1

    word_scores = []
    for word in search_space:
        unique_letters = len(set(word))
        position_score = sum(
            position_freq[i][letter] for i, letter in enumerate(word)
        )
        score = position_score * (unique_letters / 5)
        word_scores.append((score, word))

    word_scores.sort(reverse=True)
    return [word for _, word in word_scores[:5]]


def display_possible_words(
    possible_words: List[str], max_display: int = 20, show_ranking: bool = True
) -> None:
    """Display possible words after filtering, optionally ranked by relevance."""
    num_words = len(possible_words)

    if num_words == 0:
        print(f"\n{get_color('error')}✗ No possible words remain!{get_color('reset')}")
        print(
            f"   {get_color('warning')}Check your feedback entries for errors."
            f"{get_color('reset')}"
        )
        return

    if num_words == 1:
        print(
            f"\n{get_color('success')}🎉 Found the answer: "
            f"{get_color('bold')}{possible_words[0].upper()}{get_color('reset')}"
        )
        return

    if show_ranking:
        sorted_words = rank_words_by_relevance(possible_words, possible_words)
        print(
            f"\n{get_color('info')}📋 Possible words ({num_words}) - "
            f"ranked by likelihood:{get_color('reset')}"
        )
    else:
        sorted_words = sorted(possible_words)
        print(
            f"\n{get_color('info')}📋 Possible words ({num_words}) - "
            f"alphabetical:{get_color('reset')}"
        )

    display_count = min(max_display, num_words)
    cols = 4
    for i in range(0, display_count, cols):
        row_words = sorted_words[i : i + cols]
        if show_ranking and num_words > 5:
            formatted = [
                f"{j + 1:2d}.{word.upper():5s}" if j < 10 else f"   {word.upper():5s}"
                for j, word in enumerate(row_words, start=i)
            ]
        else:
            formatted = [f"{word.upper():6s}" for word in row_words]
        print(f"  {' '.join(formatted)}")

    remaining = num_words - display_count
    if remaining > 0:
        print(f"  {get_color('info')}... and {remaining} more{get_color('reset')}")


def show_statistics(possible_words: List[str]) -> None:
    """Show helpful statistics about remaining words."""
    if not possible_words:
        return

    letter_freq = Counter()
    for word in possible_words:
        letter_freq.update(word)

    print(f"\n{get_color('info')}📊 Statistics:{get_color('reset')}")
    print(
        "  Most common letters: "
        + ", ".join(letter.upper() for letter, _ in letter_freq.most_common(5))
    )

    first_letters = Counter(w[0] for w in possible_words)
    print(
        "  Most common first letters: "
        + ", ".join(letter.upper() for letter, _ in first_letters.most_common(3))
    )


def export_results(
    guesses: List[str],
    feedbacks: List[str],
    possible_words: List[str],
    filename: str = "wordle_results.txt",
) -> None:
    """Export results to a file."""
    try:
        with open(filename, "w", encoding="utf-8") as handle:
            handle.write("Wordle Solver Results\n")
            handle.write("=" * 50 + "\n\n")
            handle.write("Guesses:\n")
            for guess, feedback in zip(guesses, feedbacks):
                handle.write(f"  {guess.upper()} -> {feedback}\n")
            handle.write(f"\nPossible words ({len(possible_words)}):\n")
            for word in sorted(possible_words):
                handle.write(f"  {word.upper()}\n")
        print(
            f"\n{get_color('success')}✓ Results exported to {filename}"
            f"{get_color('reset')}"
        )
    except OSError as exc:
        print(f"\n{get_color('error')}✗ Error exporting results: {exc}{get_color('reset')}")


def configure_accessibility() -> None:
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
        choice = "1"

    if choice == "2":
        USE_HIGH_CONTRAST = True
        USE_SYMBOLS = True
    elif choice == "3":
        USE_HIGH_CONTRAST = False
        USE_SYMBOLS = False
    else:
        USE_HIGH_CONTRAST = False
        USE_SYMBOLS = True

    print(f"\n{get_color('success')}✓ Mode configured{get_color('reset')}\n")


def main() -> None:
    """Main function to run the Wordle finder."""
    print("=" * 70)
    print(
        f"{get_color('bold')}Enhanced Wordle Combinations Finder "
        f"(Colorblind-Accessible){get_color('reset')}"
    )
    print("=" * 70)

    configure_accessibility()

    word_list = load_word_list()
    word_set = set(word_list)

    print(f"{get_color('success')}✓ Loaded {len(word_list)} words{get_color('reset')}")

    print_legend()

    print(f"{get_color('bold')}Instructions:{get_color('reset')}")
    print("  - Enter your guess (5-letter word)")
    print(
        "  - Enter feedback using: G (correct position), "
        "Y (wrong position), R (not in word)"
    )
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

    guesses = []  # type: List[str]
    feedbacks = []  # type: List[str]

    while True:
        try:
            guess_input = input(
                f"{get_color('bold')}Enter guess{get_color('reset')} "
                "(or 'done'/'quit'/'undo'/'export'/'legend'): "
            ).lower().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{get_color('warning')}Exiting...{get_color('reset')}")
            break

        if guess_input in ("quit", "exit", "q"):
            print(f"{get_color('info')}Goodbye!{get_color('reset')}")
            break

        if guess_input == "legend":
            print_legend()
            continue

        if guess_input == "undo":
            if guesses:
                removed_guess = guesses.pop()
                feedbacks.pop()
                print(
                    f"{get_color('success')}✓ Removed guess: {removed_guess}"
                    f"{get_color('reset')}\n"
                )

                if guesses:
                    possible_words = filter_words(guesses, feedbacks, word_list)
                    display_known_pattern(guesses, feedbacks)
                    display_possible_words(possible_words)

                    if len(possible_words) > 5:
                        show_statistics(possible_words)
                        print(
                            f"\n{get_color('info')}💡 Suggested next guesses:"
                            f"{get_color('reset')}"
                        )
                        for word in suggest_next_guess(possible_words, word_list):
                            print(
                                f"  → {get_color('bold')}{word.upper()}"
                                f"{get_color('reset')}"
                            )
                else:
                    print(
                        f"{get_color('info')}No guesses remaining. Starting fresh!"
                        f"{get_color('reset')}\n"
                    )
            else:
                print(f"{get_color('warning')}No guesses to undo{get_color('reset')}\n")
            continue

        if guess_input == "export":
            if guesses:
                possible_words = filter_words(guesses, feedbacks, word_list)
                export_results(guesses, feedbacks, possible_words)
            else:
                print(f"{get_color('warning')}No guesses to export{get_color('reset')}\n")
            continue

        if guess_input == "done":
            break

        if guess_input not in word_set:
            print(
                f"{get_color('warning')}⚠ '{guess_input}' not in dictionary. "
                f"Continue anyway? (y/n): {get_color('reset')}",
                end="",
            )
            try:
                if input().lower().strip() != "y":
                    continue
            except (EOFError, KeyboardInterrupt):
                print()
                continue

        try:
            feedback_input = input(
                f"{get_color('bold')}Enter feedback{get_color('reset')} (G/Y/R): "
            ).upper().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{get_color('warning')}Exiting...{get_color('reset')}")
            break

        valid, error = validate_guess(guess_input, feedback_input)
        if not valid:
            print(f"{get_color('error')}✗ Error: {error}{get_color('reset')}\n")
            continue

        guesses.append(guess_input)
        feedbacks.append(feedback_input)

        print(f"  Visual: {format_feedback_display(guess_input, feedback_input)}")

        possible_words = filter_words(guesses, feedbacks, word_list)
        display_known_pattern(guesses, feedbacks)
        display_possible_words(possible_words)

        if len(possible_words) > 1 and len(possible_words) > 5:
            show_statistics(possible_words)
            print(
                f"\n{get_color('info')}💡 Suggested next guesses "
                f"(best letter coverage):{get_color('reset')}"
            )
            for word in suggest_next_guess(possible_words, word_list):
                print(f"  → {get_color('bold')}{word.upper()}{get_color('reset')}")

        print()

    if not guesses:
        print(
            f"\n{get_color('info')}📊 No guesses provided. "
            f"Total words in dictionary: {len(word_list)}{get_color('reset')}"
        )
        return

    possible_words = filter_words(guesses, feedbacks, word_list)

    print("\n" + "=" * 70)
    print(f"{get_color('bold')}FINAL RESULTS{get_color('reset')}")
    print("=" * 70)

    print(f"\n{get_color('bold')}Your guesses:{get_color('reset')}")
    for i, (guess, feedback) in enumerate(zip(guesses, feedbacks), 1):
        print(f"  {i}. {format_feedback_display(guess, feedback)}")

    display_known_pattern(guesses, feedbacks)
    display_possible_words(possible_words, max_display=50)

    if len(possible_words) > 1:
        show_statistics(possible_words)

    print("\n" + "=" * 70)

    if possible_words and len(possible_words) > 1:
        try:
            export_choice = input(
                f"\n{get_color('info')}Export results to file? (y/n): "
                f"{get_color('reset')}"
            ).lower().strip()
            if export_choice == "y":
                export_results(guesses, feedbacks, possible_words)
        except (EOFError, KeyboardInterrupt):
            print()


if __name__ == "__main__":
    main()

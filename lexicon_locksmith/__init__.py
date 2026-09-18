"""Lexicon Locksmith — colorblind-accessible Wordle solver."""

from .solver import (
    filter_words,
    is_valid_word,
    load_word_list,
    rank_words_by_relevance,
    suggest_next_guess,
    validate_guess,
)

__all__ = [
    "filter_words",
    "is_valid_word",
    "load_word_list",
    "rank_words_by_relevance",
    "suggest_next_guess",
    "validate_guess",
]

__version__ = "5.1.0"

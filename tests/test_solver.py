#!/usr/bin/env python3
"""Unit tests for Lexicon Locksmith solver (stdlib unittest)."""

import tempfile
import unittest
from pathlib import Path

from lexicon_locksmith.solver import (
    filter_words,
    is_valid_word,
    load_word_list,
    rank_words_by_relevance,
    suggest_next_guess,
    validate_guess,
)


class TestValidateGuess(unittest.TestCase):
    def test_valid(self):
        ok, err = validate_guess("crane", "GYRRR")
        self.assertTrue(ok)
        self.assertEqual(err, "")

    def test_bad_length(self):
        ok, err = validate_guess("cat", "GYR")
        self.assertFalse(ok)
        self.assertIn("5-letter", err)

    def test_bad_feedback(self):
        ok, _ = validate_guess("crane", "XXXXX")
        self.assertFalse(ok)


class TestIsValidWord(unittest.TestCase):
    def test_all_green(self):
        self.assertTrue(is_valid_word("crane", "crane", "GGGGG"))
        self.assertFalse(is_valid_word("crate", "crane", "GGGGG"))

    def test_yellow_not_same_position(self):
        # C yellow at pos 0 -> must contain C, not at 0; R/A/N/E absent
        self.assertTrue(is_valid_word("stock", "crane", "YRRRR"))
        self.assertFalse(is_valid_word("cable", "crane", "YRRRR"))  # C at 0
        self.assertFalse(is_valid_word("moist", "crane", "YRRRR"))  # no C

    def test_absent_letter(self):
        self.assertFalse(is_valid_word("apple", "crane", "RRRRR"))
        self.assertTrue(is_valid_word("moist", "crane", "RRRRR"))

    def test_duplicate_letters_green_and_absent(self):
        # Guess alley / RGRRR: L green at pos 1; second L red => exactly one L;
        # A, E, Y absent.
        self.assertTrue(is_valid_word("blimp", "alley", "RGRRR"))
        self.assertFalse(is_valid_word("allot", "alley", "RGRRR"))  # two L's + A
        self.assertFalse(is_valid_word("flail", "alley", "RGRRR"))  # two L's + A

    def test_yellow_letters_wrong_positions(self):
        # Guess speed / YYRRR: S and P present (not at 0/1); E and D absent.
        self.assertTrue(is_valid_word("pacts", "speed", "YYRRR"))
        self.assertFalse(is_valid_word("super", "speed", "YYRRR"))  # S at 0
        self.assertFalse(is_valid_word("paste", "speed", "YYRRR"))  # has E

    def test_double_letter_max_count(self):
        # Guess llama / GRRRR: L green at 0; second L red => exactly one L;
        # A/M absent.
        self.assertTrue(is_valid_word("logic", "llama", "GRRRR"))
        self.assertFalse(is_valid_word("lulls", "llama", "GRRRR"))


class TestFilterWords(unittest.TestCase):
    def setUp(self):
        self.words = [
            "crane",
            "crate",
            "trace",
            "chase",
            "close",
            "cloud",
            "apple",
        ]

    def test_filter_green_c(self):
        # C green; R/A/N/E absent
        result = filter_words(["crane"], ["GRRRR"], self.words)
        self.assertTrue(all(w[0] == "c" for w in result))
        self.assertIn("cloud", result)
        self.assertNotIn("crane", result)  # contains R/A/N/E
        self.assertNotIn("trace", result)

    def test_multi_guess(self):
        pool = ["blast", "class", "clasp", "flash", "glass", "slash"]
        # Guess slate: S yellow (not at 0), L/A green at 1/2, T/E absent
        result = filter_words(["slate"], ["YGGRR"], pool)
        self.assertIn("class", result)
        self.assertIn("glass", result)
        self.assertNotIn("slash", result)  # S at position 0
        self.assertNotIn("blast", result)  # no S
        for word in result:
            self.assertEqual(word[1], "l")
            self.assertEqual(word[2], "a")
            self.assertNotEqual(word[0], "s")
            self.assertIn("s", word)
            self.assertNotIn("t", word)
            self.assertNotIn("e", word)


class TestRanking(unittest.TestCase):
    def test_rank_prefers_common_positional_letters(self):
        words = ["aaaaa", "bcdef", "abcdf"]
        ranked = rank_words_by_relevance(words, words)
        self.assertEqual(set(ranked), set(words))
        self.assertEqual(len(ranked), 3)

    def test_suggest_returns_at_most_five(self):
        words = ["about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult"]
        suggestions = suggest_next_guess(words, words)
        self.assertLessEqual(len(suggestions), 5)
        self.assertTrue(all(s in words for s in suggestions))

    def test_suggest_small_pool(self):
        self.assertEqual(suggest_next_guess(["alone"], ["alone", "about"]), ["alone"])


class TestLoadWordList(unittest.TestCase):
    def test_loads_repo_wordlist(self):
        words = load_word_list()
        self.assertGreater(len(words), 1000)
        self.assertTrue(all(len(w) == 5 and w.isalpha() and w.islower() for w in words))
        self.assertEqual(words, sorted(set(words)))

    def test_skips_invalid_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "w.txt"
            path.write_text(
                "about\nAROUND\nxyz\nflight\nabuse\nabout\narena\n",
                encoding="utf-8",
            )
            words = load_word_list(path)
            # around/flight are 6 letters -> dropped; AROUND lowercased still 6
            self.assertEqual(words, ["about", "abuse", "arena"])


class TestFormatter(unittest.TestCase):
    def test_sanitize_and_plain_cli(self):
        from workflows.colab import formatter as fmt

        raw_words = ['"About"', "arena", "FLIGHT", "abuse", "about", "xy"]
        cleaned = fmt.sanitize_words(raw_words)
        self.assertEqual(cleaned, ["about", "abuse", "arena"])

    def test_formatter_roundtrip_file(self):
        from workflows.colab import formatter as fmt

        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "in.txt"
            out = Path(tmp) / "out.txt"
            inp.write_text('["zebra", "apple", "apple", "toolong"]\n', encoding="utf-8")
            fmt.format_wordlist(str(inp), str(out), plain=True)
            lines = out.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines, ["apple", "zebra"])


if __name__ == "__main__":
    unittest.main()

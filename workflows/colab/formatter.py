#!/usr/bin/env python3
"""
Word list formatter.

Works locally without Google Colab. Colab helpers are optional and only
available when `google.colab` is installed.

Default CLI mode writes a plain word list (one lowercase 5-letter word per
line). Use --python-list for the legacy Python-list fragment format.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

try:
    from google.colab import files as colab_files  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    colab_files = None


def _extract_tokens(raw: str) -> List[str]:
    """Pull words from either one-per-line text or Python-list fragments."""
    quoted = re.findall(r'"([A-Za-z]+)"|\'([A-Za-z]+)\'', raw)
    if quoted:
        return [a or b for a, b in quoted]
    return [line.strip() for line in raw.splitlines() if line.strip()]


def sanitize_words(
    words: List[str],
    *,
    five_letter_only: bool = True,
    alphabetize: bool = True,
) -> List[str]:
    """Deduplicate, lowercase, and optionally keep only 5-letter alpha words."""
    seen = set()
    unique: List[str] = []
    for word in words:
        cleaned = word.strip().lower()
        if not cleaned.isalpha():
            continue
        if five_letter_only and len(cleaned) != 5:
            continue
        if cleaned not in seen:
            seen.add(cleaned)
            unique.append(cleaned)
    if alphabetize:
        unique.sort()
    return unique


def format_as_python_list(words: List[str], words_per_line: int = 10) -> str:
    """Format words as a Python list literal (legacy helper output)."""
    lines = ["[\n"]
    for i in range(0, len(words), words_per_line):
        chunk = words[i : i + words_per_line]
        formatted_chunk = ", ".join(f'"{word}"' for word in chunk)
        if i + words_per_line < len(words):
            lines.append(f"    {formatted_chunk},\n")
        else:
            lines.append(f"    {formatted_chunk}\n")
    lines.append("]\n")
    return "".join(lines)


def format_as_plain_list(words: List[str]) -> str:
    """Format words as one lowercase word per line."""
    return "\n".join(words) + ("\n" if words else "")


def format_wordlist(
    input_file,
    output_file="formatted_words.txt",
    words_per_line=10,
    alphabetize=True,
    *,
    plain: bool = False,
    five_letter_only: bool = True,
):
    """
    Read words from input file and write a formatted word list.

    By default writes a Python list (historical Colab behavior). Pass
    plain=True (or use the CLI) for one-word-per-line output suitable for
    the canonical solver's wordlist.txt.
    """
    raw = Path(input_file).read_text(encoding="utf-8")
    unique_words = sanitize_words(
        _extract_tokens(raw),
        five_letter_only=five_letter_only,
        alphabetize=alphabetize,
    )

    if plain:
        content = format_as_plain_list(unique_words)
    else:
        content = format_as_python_list(unique_words, words_per_line=words_per_line)

    Path(output_file).write_text(content, encoding="utf-8")

    print(f"✓ Formatted {len(unique_words)} unique words")
    print(f"✓ Output saved to: {output_file}")
    if unique_words:
        print(f"\nFirst few words: {', '.join(unique_words[:5])}")
        print(f"Last few words: {', '.join(unique_words[-5:])}")

    return output_file


def quick_format(input_file, alphabetize=True, plain: bool = False):
    """Quick format that prints to console."""
    raw = Path(input_file).read_text(encoding="utf-8")
    unique_words = sanitize_words(
        _extract_tokens(raw),
        five_letter_only=True,
        alphabetize=alphabetize,
    )
    if plain:
        print(format_as_plain_list(unique_words), end="")
    else:
        print(format_as_python_list(unique_words), end="")
    return unique_words


def upload_wordlist():
    """Upload a wordlist file from your computer (Colab only)."""
    if colab_files is None:
        raise RuntimeError(
            "google.colab is not available. "
            "Run this script locally with: python formatter.py INPUT -o OUTPUT"
        )
    uploaded = colab_files.upload()
    filename = list(uploaded.keys())[0]
    print(f"✓ Uploaded: {filename}")
    return filename


def download_file(filepath):
    """Download a file from Colab to your computer (Colab only)."""
    if colab_files is None:
        raise RuntimeError(
            "google.colab is not available. "
            "Copy the output file from disk instead."
        )
    colab_files.download(filepath)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Format a Wordle word list (stdlib CLI; Colab optional)."
    )
    parser.add_argument("input", help="Input word list (plain lines or list fragments)")
    parser.add_argument(
        "-o",
        "--output",
        default="formatted_words.txt",
        help="Output path (default: formatted_words.txt)",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        default=True,
        help="Write one lowercase word per line (default)",
    )
    parser.add_argument(
        "--python-list",
        action="store_true",
        help="Write a Python list literal instead of plain lines",
    )
    parser.add_argument(
        "--no-sort",
        action="store_true",
        help="Keep first-seen order instead of sorting",
    )
    parser.add_argument(
        "--keep-non-five",
        action="store_true",
        help="Keep alphabetic words that are not length 5",
    )
    parser.add_argument(
        "--words-per-line",
        type=int,
        default=10,
        help="Words per line when using --python-list",
    )
    args = parser.parse_args(argv)

    plain = not args.python_list
    format_wordlist(
        args.input,
        output_file=args.output,
        words_per_line=args.words_per_line,
        alphabetize=not args.no_sort,
        plain=plain,
        five_letter_only=not args.keep_non_five,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

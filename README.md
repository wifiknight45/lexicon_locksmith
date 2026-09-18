[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Accessibility](https://img.shields.io/badge/accessibility-colorblind%20friendly-brightgreen.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![Deutanopia](https://img.shields.io/badge/optimized-deutanopia-blue.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Wordle](https://img.shields.io/badge/game-Wordle%20solver-success.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-success.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![High Contrast](https://img.shields.io/badge/display-high%20contrast%20mode-orange.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![Symbol Support](https://img.shields.io/badge/symbols-visual%20encoding-purple.svg)](https://github.com/wifiknight45/lexicon_locksmith)

## Lexicon Locksmith - Wordle Combinations Finder

A colorblind-accessible Wordle helper that filters possible solutions from your guesses and feedback (G/Y/R). Includes letter-frequency ranking and three display modes optimized for deutanopia.

The **canonical Python solver** is the accessibility v5 logic (ranking + accessibility modes), packaged so you do not need to dig under `accessibility/v5/`.

## Prerequisites

- Python 3.7 or higher
- No third-party packages required (stdlib only)

## Installation

```bash
git clone https://github.com/wifiknight45/lexicon_locksmith.git
cd lexicon_locksmith
```

## Usage (canonical entrypoint)

Any of these run the same solver:

```bash
python wordle_combo_finder.py
python -m lexicon_locksmith
```

At startup, pick a display mode:

1. Standard (blue / magenta / gray with symbols)
2. High contrast
3. Colors only (no symbols)

Then enter each guess and feedback:

- **G** = correct letter, correct position
- **Y** = correct letter, wrong position
- **R** = letter not in the word (or excess duplicate)

Commands: `done`, `undo`, `export`, `legend`, `quit`

### Word list

`wordlist.txt` at the repo root is the source of truth: **one lowercase 5-letter alphabetic word per line**, deduplicated and sorted. The solver loads this file from disk (no embedded 600-line list).

Optional helper to reformat a list (works without Colab):

```bash
python workflows/colab/formatter.py some_words.txt -o wordlist.txt --plain
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

| Path | Role |
|------|------|
| `wordle_combo_finder.py` | **Canonical CLI entrypoint** (thin wrapper) |
| `lexicon_locksmith/` | Canonical package (solver + wordlist loading) |
| `wordlist.txt` | Sanitized on-disk word list |
| `workflows/colab/formatter.py` | Word-list formatter (stdlib CLI; Colab optional) |
| `tests/` | Unit tests |
| `wordle_combo_script.py` | **Legacy** root script (embedded list) |
| `accessibility/v1` … `v5/` | **Archive / legacy** accessibility iterations |
| `v1/` | **Archive / legacy** C#, VB, early Python |

## Legacy / archive

Older versions under `accessibility/`, `v1/`, and `wordle_combo_script.py` are kept for history. Prefer `wordle_combo_finder.py` / `python -m lexicon_locksmith` for day-to-day use.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

- Inspired by Wordle by Josh Wardle
- Word list thanks to [@darkermango](https://github.com/darkermango)
- Optimized for deutanopia based on colorblind accessibility research

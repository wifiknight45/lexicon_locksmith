
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Accessibility](https://img.shields.io/badge/accessibility-colorblind%20friendly-brightgreen.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![Deutanopia](https://img.shields.io/badge/optimized-deutanopia-blue.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Wordle](https://img.shields.io/badge/game-Wordle%20solver-success.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-success.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![High Contrast](https://img.shields.io/badge/display-high%20contrast%20mode-orange.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![Symbol Support](https://img.shields.io/badge/symbols-visual%20encoding-purple.svg)](https://github.com/wifiknight45/lexicon_locksmith)
## Lexicon Locksmith - Wordle Combinations Finder

A powerful, intelligent Python script that helps you solve Wordle puzzles by filtering possible word combinations based on your guesses and feedback. Perfect for Wordle enthusiasts who want to improve their game strategy. Please note this Readme.md is geared for the python script but there are also versions in C# and Visual Basic etc.

## Accessibility: 
Please note that an updated version of the python script is now avaliable for those with visibility impairments inlcuding colorblindness (deutanopia specifically). Please see the folder titled "accessibility" to run it at: "accessibility/deutan_wordle_combo_finder.py" thank you. 


## Features

Accurate Word Filtering - Handles complex scenarios including duplicate letters

Comprehensive Dictionary - 500+ common 5-letter English words

Smart Suggestions - AI-powered recommendations for your next guess based on letter frequency analysis

Fast Performance - Efficient filtering algorithm processes possibilities instantly

Clean Interface - Formatted output with clear visual indicators

Real-time Feedback - See remaining possibilities after each guess

Robust Error Handling - Validates input and provides helpful error messages

## Quick Start

## Prerequisites

Python 3.6 or higher

## Installation

1) Clone the repository:

bash
git clone https://github.com/wifiknight45/lexicon_locksmith.git
cd lexicon_locksmith

2) Run the script (choose your desired version):

bash

'wordle_combo_finder.cs' v1 (standard version)
'wordle_combo_finder.vb' v1
'wordle_combo_script.py' v1

or 

'deutan_wordle_combo_finder.py' v2 (accessibility version)

or 

**best option: 'wordle_combo_finder.py' - v3 (accessibility version + enhanced wordlist)**

please note that the above 'wordle_combo_finder.py is still under dev as the word list needs to be manually formatted and I only have
so much time to dedicate to it etc.


That's it. No external dependencies required ;-)

## How to Use
Basic Usage

Start the script and you'll see the welcome screen
Enter your guess - any 5-letter word you tried in Wordle
Enter the feedback using these codes:

G = Green (correct letter, correct position)
Y = Yellow (correct letter, wrong position)
R = Red (letter not in word)


Repeat for each guess you've made
Type 'done' when finished to see all possible words

----------------------------------------------

Example Session
Enhanced Wordle Combinations Finder
============================================

Instructions:
  - Enter your guess (5-letter word)
  - Enter feedback: G (green), Y (yellow), R (red)
  - Type 'done' when finished entering guesses
  - Type 'quit' to exit

Example:
  Guess: crane
  Feedback: GYRRR (C is green, R is yellow, rest are red)

Enter guess (or 'done'/'quit'): crane
Enter feedback (G/Y/R): GYRRR
✓ Added guess. Remaining possibilities: 87

Enter guess (or 'done'/'quit'): cloth
Enter feedback (G/Y/R): GRRYR
✓ Added guess. Remaining possibilities: 12

Enter guess (or 'done'/'quit'): done

============================================================
RESULTS
============================================================

✓ Found 12 possible word(s):

   1. CABBY
   2. CADDY
   3. CAMPY
   4. CARBS
   5. CARGO
   6. CARRY
   7. CATTY
   8. CURVY
   ...

💡 Suggested next guesses (best letter coverage):
  → CARGO
  → CARRY
  → CURVY

============================================================
Wordle Feedback Guide
Understanding the feedback colors in Wordle:
ColorCodeMeaningExampleGreenGCorrect letter in correct positionIf you guess "CRANE" and C is green, the word starts with CYellowYCorrect letter in wrong positionIf you guess "CRANE" and R is yellow, R exists but not in position 2Gray/RedRLetter not in the wordIf you guess "CRANE" and A is gray, A doesn't appear in the word
Important Note: If a letter appears multiple times in your guess, pay attention to each occurrence:

"SPEED" with feedback "GRRRG" means S is correct, E is correct at the end, but the middle E and P are not in the word

Algorithm Details
The script uses a sophisticated filtering algorithm:

Green Letter Matching - Ensures letters marked green are in the exact position
Yellow Letter Validation - Confirms yellows exist in the word but NOT in the guessed position
Red Letter Elimination - Removes words containing letters marked red (accounting for duplicates)
Frequency Analysis - Suggests next guesses based on which words test the most uncovered letters

## Advanced Features
letter Frequency Suggestions
**When multiple possibilities remain, the script analyzes letter frequency across all remaining words and suggests guesses that will eliminate the most possibilities:
Suggested next guesses (best letter coverage):
  → STARE  # Tests common letters S, T, A, R, E
  → SLATE  # Tests common letters S, L, A, T, E

Duplicate Letter Handling
The script correctly handles words with duplicate letters:

Word: "SPEED"
Guess: "ERASE" with feedback "YRRRG"
Correctly identifies E appears twice but not where guessed

## Statistics
a) Dictionary Size: 500+ carefully curated common English words
b) Average Filter Time: < 0.01 seconds
c) Accuracy: 100% for valid Wordle solutions
c) Supported Word Length: 5 letters (standard Wordle format)

## Contributing
Contributions are welcome. Here's how you can help:

## Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

## Ideas for Contributions

a) Expand the word dictionary
b) Add support for Wordle variations (6-letter, themed words, etc.)
c) Implement word difficulty scoring
d) Add statistics tracking (average guesses to solve, etc.)
e) Create a GUI version
f) Add support for other languages

## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments

a) Inspired by the popular Wordle game by Josh Wardle.
b) The word list used was curated from common English language dictionaries.
c) A huge thank you to @darkermango (https://github.com/darkermango) for the sweet wordlist.


## Contact

wifiknight45@proton.me
Project Link: https://github.com/wifiknight45/lexicon_locksmith
Script Link: wordle_combo_script.py 


## If you find this tool helpful, please consider giving it a star.

## Happy Wordling
designed for wordle enthusiasts and techies alike

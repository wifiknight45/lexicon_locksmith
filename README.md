
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

a) Accurate Word Filtering - Handles complex scenarios including duplicate letters

b) Comprehensive Dictionary - 2,000+ common 5-letter English words

c) Smart Suggestions - AI-powered recommendations for your next guess based on letter frequency analysis

d) Fast Performance - Efficient filtering algorithm processes possibilities instantly

f) Clean Interface - Formatted output with clear visual indicators

g) Real-time Feedback - See remaining possibilities after each guess

h) Robust Error Handling - Validates input and provides helpful error messages


## Prerequisites

Python 3.6 or higher


## Installation

1) Clone the repository:

bash

git clone https://github.com/wifiknight45/lexicon_locksmith.git

cd lexicon_locksmith


2) Run the script:

bash

'wordle_combo_finder.py' - v3 (accessibility version + enhanced wordlist)**

That's it. No external dependencies required ;-)

## How to Use
Basic Usage

a) Start the script and you'll see the welcome screen

b) Enter your guess - any 5-letter word you tried in Wordle

c) Enter the feedback using these codes:

G = Green (correct letter, correct position)
Y = Yellow (correct letter, wrong position)
R = Red (letter not in word)


Repeat for each guess you've made
Type 'done' when finished to see all possible words



## Happy Wordling
designed for students, techies and wordle enthusiasts 

========
Wordle Solver - Colorblind-Accessible Edition

A powerful, accessible command-line tool for solving Wordle puzzles with enhanced support for colorblind users, particularly those with deutanopia (red-green colorblindness).

Features
a) Accessibility First

b) Deutanopia-optimized color scheme: Uses blue, magenta, and gray instead of traditional green, yellow, and red

c) Three display modes:

  i.   Standard mode (colors + symbols)
  
  ii.  High contrast mode (enhanced backgrounds + symbols)
  
  iii. Colors-only mode (for users who prefer no symbols)

d) Visual symbols: Each letter state has a unique symbol (█ ○ ·) for additional distinction

e) Clear legend: Always available to reference color meanings

## Intelligent Solving

Smart word filtering: Handles complex constraints including duplicate letters
Pattern visualization: Shows known letters and their positions
Next-guess suggestions: Recommends optimal guesses based on letter frequency analysis
Statistics: Displays helpful insights about remaining possibilities
Large word database: Over 5,000+ common 5-letter English words

## User-Friendly Features

Interactive interface: Step-by-step guidance through the solving process
Undo functionality: Remove incorrect guesses easily
Export results: Save your solving session to a text file
Input validation: Catches errors before processing
Dictionary checking: Warns about words not in the database

## Installation
Requirements

Python 3.6 or higher
No external dependencies required (uses only Python standard library)

## Setup

Download the script:

bashwget https://your-url/wordle_solver.py
# or
curl -O https://your-url/wordle_solver.py

Make it executable (Unix/Linux/Mac):

bashchmod +x wordle_solver.py

Run it:

bashpython3 wordle_solver.py
# or
./wordle_solver.py
Usage
Quick Start

Launch the program:

bashpython3 wordle_solver.py

Choose your accessibility mode:

Mode 1: Standard (recommended for most users)
Mode 2: High contrast (for enhanced visibility)
Mode 3: No symbols (colors only)


Enter your guesses:

Type a 5-letter word (e.g., crane)
Enter the feedback using:

G = Green (correct position)
Y = Yellow (wrong position)
R = Red (not in word)




Get results:

View possible words
See pattern analysis
Get next-guess suggestions



Example Session
Enter guess: crane
Enter feedback: GYRRR

  Visual: █C ○R ·A ·N ·E
✓ Added guess. Remaining possibilities: 234

Known Pattern: C _ _ _ _
Must contain: R
Cannot contain: A, N, E

Enter guess: court
Enter feedback: GRGRG

  Visual: █C ·O ·U █R █T
✓ Added guess. Remaining possibilities: 1

RESULTS
========================================
Found 1 possible word:

  1. CRYPT
Commands
During the solving process, you can use these commands:
CommandDescriptiondoneFinish entering guesses and see resultsundoRemove the last guessexportSave results to wordle_results.txtlegendDisplay the color/symbol guide againquit / exit / qExit the program
Understanding Feedback
Color Scheme
Standard Mode:

🟦 Blue (█): Letter is correct and in the right position
🟪 Magenta (○): Letter is in the word but wrong position
⬛ Gray (·): Letter is not in the word

High Contrast Mode:

Same meanings with enhanced backgrounds for better visibility

Handling Duplicate Letters
The solver correctly handles words with duplicate letters:
Example: If you guess SPEED and the answer is STEEL:

First E: Yellow (wrong position)
Second E: Green (correct position)
Other letters: Based on their status

Advanced Features
Pattern Analysis
The tool shows you:

Known positions: Letters confirmed in specific spots
Must contain: Letters that are in the word but position unknown
Cannot contain: Letters that aren't in the word

Next-Guess Suggestions
When multiple words are possible, the tool suggests guesses that will:

Eliminate the most possibilities
Use high-frequency letters in common positions
Maximize information gain

Statistics
View helpful insights:

Most common letters in remaining words
Most common first letters
Letter frequency distribution

Export Functionality
Save your solving session including:

All guesses and their feedback
Complete list of possible words
Formatted for easy reference

Tips for Best Results

Start with common letters: Words like CRANE, SLATE, or AROSE are good openers
Use the undo feature: If you make a typo, just type undo
Trust the suggestions: When many words remain, the suggested guesses are optimized for information gain
Check the pattern: The visual pattern helps verify your input is correct
Export before closing: Save your results for future reference

Technical Details
Algorithm
The solver uses:

Constraint satisfaction: Filters words based on position and presence constraints
Frequency analysis: Scores words by letter frequency in remaining possibilities
Duplicate letter handling: Correctly interprets feedback for repeated letters

Performance

Processes 5,000+ words instantly
Handles complex constraint combinations
Optimized for minimal memory usage

Compatibility

Operating Systems: Linux, macOS, Windows
Terminals: Any terminal with ANSI color support
Python Versions: 3.6+

Accessibility Considerations
This tool was designed with accessibility in mind:

Colorblind-friendly: Uses blue/magenta/gray instead of green/yellow/red
Multiple visual cues: Colors + symbols + text descriptions
Keyboard-only operation: No mouse required
Clear instructions: Step-by-step guidance
Configurable display: Choose what works best for you

Troubleshooting
Colors not displaying correctly

Ensure your terminal supports ANSI colors
Try high contrast mode (option 2)
Use colors-only mode (option 3) if symbols don't render

Word not in dictionary

The tool will warn you but allow you to continue
Most common Wordle words are included
You can still solve with words outside the dictionary

No matches found

Double-check your feedback entries
Use undo to correct mistakes
Ensure G/Y/R are entered correctly

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
a) Inspired by the popular Wordle game by Josh Wardle.
b) A huge thank you to @darkermango (https://github.com/darkermango) for the sweet wordlist.
c) Optimized for deutanopia based on colorblind accessibility research


Version: 3.0

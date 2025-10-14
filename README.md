
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Accessibility](https://img.shields.io/badge/accessibility-colorblind%20friendly-brightgreen.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![Deutanopia](https://img.shields.io/badge/optimized-deutanopia-blue.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Wordle](https://img.shields.io/badge/game-Wordle%20solver-success.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-success.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![High Contrast](https://img.shields.io/badge/display-high%20contrast%20mode-orange.svg)](https://github.com/wifiknight45/lexicon_locksmith)
[![Symbol Support](https://img.shields.io/badge/symbols-visual%20encoding-purple.svg)](https://github.com/wifiknight45/lexicon_locksmith)
## Lexicon Locksmith - Wordle Combinations Finder

A powerful, intelligent Python script that aids in solving Wordle puzzles by filtering possible word combinations based on your guesses and feedback. Perfect for Wordle enthusiasts who want to improve their game strategy. Please note this Readme.md is geared for the python script but there are also versions in C# and Visual Basic etc.

## Accessibility: 
Please note that an updated version (i.e. v3) of the python script is now avaliable for those with visibility impairments inlcuding colorblindness (deutanopia specifically). Please see the folder titled "accessibility" to run it at: "accessibility/v3/wordle_combo_finder.py" thank you. 


## Features

a) Accurate Word Filtering - Handles complex scenarios including duplicate letters

b) Comprehensive Dictionary - 2,000+ common 5-letter English words

c) Smart Suggestions - AI-powered recommendations for your next guess based on letter frequency analysis

d) Fast Performance - Efficient filtering algorithm processes possibilities instantly

f) Clean Interface - Formatted output with clear visual indicators

g) Real-time Feedback - See remaining possibilities after each guess

h) Robust Error Handling - Validates input and provides helpful error messages

i) Three display modes:

    i. Standard mode (colors + symbols)

    ii. High contrast mode (enhanced backgrounds + symbols)

    iii. Colors-only mode (for users who prefer no symbols)



## Prerequisites

Python 3.6 or higher


## Installation

1) Clone the repository:

bash

**'git clone https://github.com/wifiknight45/lexicon_locksmith.git'**

**'cd lexicon_locksmith'**


2) Run the script:

bash

**'wordle_combo_finder.py' - v3 (accessibility version + enhanced wordlist)**

That's it. No external dependencies required ;-)

## How to Use

a) Start the script and you'll see the welcome screen

b) Enter your guess - any 5-letter word you tried in Wordle

c) Enter the feedback using these codes:

G = Green (correct letter, correct position)
Y = Yellow (correct letter, wrong position)
R = Red (letter not in word)

Repeat for each guess you've made
Type 'done' when finished to see all possible words


## Happy Wordlin
designed with love in california for students, techies and wordle enthusiasts 


## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments
a) Inspired by the popular Wordle game by Josh Wardle.

b) A huge thank you to @darkermango (https://github.com/darkermango) for the sweet wordlist.

c) Optimized for deutanopia based on colorblind accessibility research

d) developed using anthropic claude.ai sonnet 4.5 + microsoft copilot gpt-5 


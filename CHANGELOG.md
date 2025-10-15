v5 updates
Added rank_words_by_relevance() function - Scores words based on:

Positional letter frequency (most important - letters common in their specific positions)
Overall letter frequency (letters that appear frequently across remaining words)
Unique letters bonus (words with more unique letters give better information)
Commonality proxy (words earlier in the list tend to be more common)


Updated display_possible_words() to:

Call the ranking function by default
Show ranking numbers (1, 2, 3...) for top results
Add show_ranking parameter to optionally show alphabetically


How It Works:

Most relevant words appear first based on letter frequency analysis
Top 10 words show ranking numbers (1. WORD, 2. WORD, etc.)
The algorithm prioritizes words whose letters appear frequently in the exact positions among remaining possibilities
--
Key Improvements Made re: 
1. Deutanopia-Friendly Colors

Blue instead of green for correct positions
Magenta instead of yellow for wrong positions
Gray for absent letters
These colors are clearly distinguishable for people with red-green colorblindness

2. High Contrast Mode

White text on colored backgrounds for maximum visibility
User can choose between standard and high-contrast at startup

3. Symbol Support

█ (solid block) for correct position
○ (circle) for wrong position
· (dot) for absent letters
Provides redundant encoding beyond just color

4. Accessibility Configuration

Mode selection at startup
Three options: standard, high-contrast, or colors-only
Remembers preference during session

5. Visual Feedback

Shows formatted display of each guess immediately after entry
Summary view at the end showing all guesses visually
Interactive legend command

#!/usr/bin/env python3
"""
Format a word list into Python list format with quoted strings
"""

def format_wordlist(input_file, output_file, words_per_line=10, alphabetize=True):
    """
    Read words from input file and format them as a Python list.
    
    Args:
        input_file: Path to input text file (one word per line)
        output_file: Path to output file
        words_per_line: Number of words to display per line (default: 10)
        alphabetize: Whether to sort words alphabetically (default: True)
    """
    # Read all words from the file
    with open(input_file, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
    
    # Remove duplicates and convert to lowercase
    seen = set()
    unique_words = []
    for word in words:
        if word.lower() not in seen:
            seen.add(word.lower())
            unique_words.append(word.lower())
    
    # Alphabetize if requested
    if alphabetize:
        unique_words.sort()
    
    # Format the output
    formatted_lines = []
    formatted_lines.append('[\n')
    
    # Process words in chunks
    for i in range(0, len(unique_words), words_per_line):
        chunk = unique_words[i:i + words_per_line]
        # Format each word with quotes
        formatted_chunk = ', '.join(f'"{word}"' for word in chunk)
        
        # Add comma at the end if not the last line
        if i + words_per_line < len(unique_words):
            formatted_lines.append(f'    {formatted_chunk},\n')
        else:
            formatted_lines.append(f'    {formatted_chunk}\n')
    
    formatted_lines.append(']\n')
    
    # Write to output file
    with open(output_file, 'w') as f:
        f.writelines(formatted_lines)
    
    print(f"✓ Formatted {len(unique_words)} unique words")
    print(f"✓ Output saved to: {output_file}")
    print(f"\nFirst few words: {', '.join(unique_words[:5])}")
    print(f"Last few words: {', '.join(unique_words[-5:])}")


def quick_format(input_file, alphabetize=True):
    """Quick format that prints to console."""
    with open(input_file, 'r') as f:
        words = [line.strip().lower() for line in f if line.strip()]
    
    # Remove duplicates
    unique_words = list(dict.fromkeys(words))
    
    # Alphabetize if requested
    if alphabetize:
        unique_words.sort()
    
    print('[')
    for i in range(0, len(unique_words), 10):
        chunk = unique_words[i:i + 10]
        formatted = ', '.join(f'"{word}"' for word in chunk)
        if i + 10 < len(unique_words):
            print(f'    {formatted},')
        else:
            print(f'    {formatted}')
    print(']')
    
    return unique_words


# Example usage
if __name__ == "__main__":
    import sys
    
    print("Word List Formatter")
    print("=" * 50)
    
    # Get input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = input("Enter input file name (e.g., wordlist.txt): ").strip()
    
    # Get output file
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = input("Enter output file name (e.g., formatted_words.txt): ").strip()
        if not output_file:
            output_file = "formatted_words.txt"
    
    # Get words per line
    try:
        words_per_line = int(input("Words per line (default 10): ").strip() or "10")
    except ValueError:
        words_per_line = 10
    
    print("\nProcessing...\n")
    
    try:
        format_wordlist(input_file, output_file, words_per_line)
        print(f"\n✓ Done! Check {output_file}")
    except FileNotFoundError:
        print(f"✗ Error: File '{input_file}' not found")
    except Exception as e:
        print(f"✗ Error: {e}")

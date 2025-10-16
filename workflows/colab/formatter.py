# Word List Formatter (Colab-friendly)

from google.colab import files

def format_wordlist(input_file, output_file="formatted_words.txt", words_per_line=10, alphabetize=True):
    """
    Read words from input file and format them as a Python list.
    
    Args:
        input_file: Path to input text file (one word per line)
        output_file: Path to output file (default: formatted_words.txt)
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
    
    for i in range(0, len(unique_words), words_per_line):
        chunk = unique_words[i:i + words_per_line]
        formatted_chunk = ', '.join(f'"{word}"' for word in chunk)
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
    
    return output_file


def quick_format(input_file, alphabetize=True):
    """Quick format that prints to console."""
    with open(input_file, 'r') as f:
        words = [line.strip().lower() for line in f if line.strip()]
    
    unique_words = list(dict.fromkeys(words))
    
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


# --- Helper functions for Colab ---

def upload_wordlist():
    """Upload a wordlist file from your computer."""
    uploaded = files.upload()
    filename = list(uploaded.keys())[0]
    print(f"✓ Uploaded: {filename}")
    return filename

def download_file(filepath):
    """Download a file from Colab to your computer."""
    files.download(filepath)

import json
from collections import Counter
import re

def extract_words(text):
    # Convert to lowercase and split into words
    # Remove special characters and numbers
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return words

def main():
    # Read the JSON file
    with open('anime_data.JSON', 'r', encoding='utf-8') as file:
        anime_data = json.load(file)
    
    # Collect all words from all fields
    all_words = []
    for anime in anime_data:
        # Process each field that might contain text
        for value in anime.values():
            if isinstance(value, str):
                all_words.extend(extract_words(value))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        all_words.extend(extract_words(item))
    
    # Count word occurrences
    word_counts = Counter(all_words)
    
    # Filter words that appear more than once
    repeated_words = {word: count for word, count in word_counts.items() if count > 1}
    
    # Sort by count in descending order
    sorted_words = sorted(repeated_words.items(), key=lambda x: x[1], reverse=True)
    
    # Print results
    print("\nWords that appear more than once in the anime data:")
    print("-" * 50)
    for word, count in sorted_words:
        print(f"{word}: {count} times")
    
    print(f"\nTotal number of repeated words: {len(repeated_words)}")

if __name__ == "__main__":
    main() 
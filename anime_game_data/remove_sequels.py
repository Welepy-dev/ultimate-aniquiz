import json
import re

def is_sequel(name):
    # Common sequel indicators
    sequel_patterns = [
        r'season\s+\d+',
        r'part\s+\d+',
        r'\d+(?:st|nd|rd|th)\s+season',
        r'2nd',
        r'3rd',
        r'4th',
        r'5th',
        r'6th',
        r'7th',
        r'8th',
        r'9th',
        r'10th',
        r'sequel',
        r'next\s+generation',
        r'new\s+series',
        r'continued',
        r'final',
        r'last',
        r'conclusion',
        r'ending'
    ]
    
    # Check if any of the patterns match the name (case insensitive)
    return any(re.search(pattern, name.lower()) for pattern in sequel_patterns)

def main():
    # Read the JSON file
    with open('anime_data.JSON', 'r', encoding='utf-8') as file:
        anime_data = json.load(file)
    
    # Filter out sequels
    original_anime = [anime for anime in anime_data if not is_sequel(anime['name'])]
    
    # Save the filtered data back to the file
    with open('anime_data.JSON', 'w', encoding='utf-8') as file:
        json.dump(original_anime, file, indent=2, ensure_ascii=False)
    
    # Print statistics
    print(f"Original number of entries: {len(anime_data)}")
    print(f"Number of entries after removing sequels: {len(original_anime)}")
    print(f"Number of sequels removed: {len(anime_data) - len(original_anime)}")

if __name__ == "__main__":
    main() 
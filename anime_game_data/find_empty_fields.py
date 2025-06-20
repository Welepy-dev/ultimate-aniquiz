import json

def is_empty_value(value):
    if value is None:
        return True
    if isinstance(value, str) and (value.lower() == 'unknown' or value.strip() == ''):
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False

def main():
    # Read the JSON file
    with open('anime_data.JSON', 'r', encoding='utf-8') as file:
        anime_data = json.load(file)
    
    # Track entries with empty fields
    entries_with_empty_fields = []
    
    # Check each anime entry
    for index, anime in enumerate(anime_data):
        empty_fields = []
        
        # Check each field in the entry
        for field, value in anime.items():
            if is_empty_value(value):
                empty_fields.append(field)
        
        # If any empty fields were found, add to our list
        if empty_fields:
            entries_with_empty_fields.append({
                'index': index,
                'name': anime.get('name', 'Unknown Title'),
                'empty_fields': empty_fields
            })
    
    # Print results
    print("\nEntries with empty, null, or unknown fields:")
    print("-" * 50)
    
    if not entries_with_empty_fields:
        print("No entries found with empty fields!")
    else:
        for entry in entries_with_empty_fields:
            print(f"\nAnime: {entry['name']}")
            print(f"Empty fields: {', '.join(entry['empty_fields'])}")
    
    print(f"\nTotal entries with empty fields: {len(entries_with_empty_fields)}")
    print(f"Total entries in dataset: {len(anime_data)}")

if __name__ == "__main__":
    main() 
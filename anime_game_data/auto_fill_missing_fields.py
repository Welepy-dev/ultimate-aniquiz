import json
import re
import requests
from bs4 import BeautifulSoup

# File paths
JSON_PATH = 'anime_data.JSON'
EMPTY_PATH = 'empty.txt'

# Helper: Search MyAnimeList for anime and get its page URL
def search_mal(anime_name):
    search_url = f'https://myanimelist.net/anime.php?q={requests.utils.quote(anime_name)}'
    resp = requests.get(search_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Find the first anime result
    result = soup.find('a', href=re.compile(r'/anime/\\d+'))
    if result:
        return result['href']
    return None

# Helper: Scrape MAL page for a field
def scrape_mal_field(mal_url, field):
    resp = requests.get(mal_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Map field to MAL label
    field_map = {
        'year': 'Aired:',
        'season': 'Premiered:',
        'demographic': 'Demographic:',
        'theme': 'Theme:',
    }
    label = field_map.get(field)
    if not label:
        return 'UNKNOWN'
    info = soup.find('span', string=label)
    if info:
        # Get the next sibling text
        value = info.find_next_sibling(text=True)
        if value:
            value = value.strip()
            # For demographic/theme, return as list
            if field in ['demographic', 'theme']:
                return [v.strip() for v in value.split(',')]
            # For year, extract year
            if field == 'year':
                m = re.search(r'(\\d{4})', value)
                return int(m.group(1)) if m else 'UNKNOWN'
            # For season, extract season name
            if field == 'season':
                return value.split(' ')[0].lower()
            return value
    return 'UNKNOWN'

# Step 1: Parse empty.txt
with open(EMPTY_PATH, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

missing = []  # List of (anime_name, [fields])
anime = None
for line in lines:
    if line.startswith('Anime: '):
        anime = line.replace('Anime: ', '').strip()
    elif line.startswith('Empty fields:') and anime:
        fields = [f.strip() for f in line.replace('Empty fields:', '').split(',')]
        missing.append((anime, fields))
        anime = None

# Step 2: Load anime_data.JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Step 3: For each missing field, try to fill it
for anime_name, fields in missing:
    # Find anime in data
    anime_entry = next((a for a in data if a['name'] == anime_name), None)
    if not anime_entry:
        print(f"Anime '{anime_name}' not found in JSON.")
        continue
    print(f"Filling fields for: {anime_name}")
    mal_url = search_mal(anime_name)
    if not mal_url:
        print(f"  Could not find MAL page for {anime_name}")
        for field in fields:
            anime_entry[field] = 'UNKNOWN'
        continue
    for field in fields:
        value = scrape_mal_field(mal_url, field)
        anime_entry[field] = value
        print(f"  {field}: {value}")

# Step 4: Save updated JSON
def default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2, default=default)

print('Done!') 
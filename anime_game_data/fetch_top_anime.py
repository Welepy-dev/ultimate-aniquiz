import requests
import time
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import re

# Constants
API_URL = 'https://api.jikan.moe/v4/top/anime'
DETAIL_URL = 'https://api.jikan.moe/v4/anime/{}'
PER_PAGE = 25
TOTAL = 1200
PAGES = TOTAL // PER_PAGE
OUTPUT_FILE = 'anime_data.JSON'
RATE_LIMIT = 0.4  # 3 requests/sec

# Helper functions
def get_top_anime(page):
    params = {'page': page, 'limit': PER_PAGE}
    resp = requests.get(API_URL, params=params)
    time.sleep(RATE_LIMIT)
    resp.raise_for_status()
    return resp.json()['data']

def get_anime_details(mal_id):
    resp = requests.get(DETAIL_URL.format(mal_id))
    time.sleep(RATE_LIMIT)
    resp.raise_for_status()
    return resp.json()['data']

def get_country_of_origin(anime):
    # Try to infer from studios or external links
    studios = anime.get('studios', [])
    if studios:
        for studio in studios:
            if 'Japan' in studio.get('name', ''):
                return 'Japan'
    # Try to scrape MyAnimeList page
    url = anime.get('url')
    if url:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            info = soup.find('div', {'id': 'content'}).text
            if 'Japan' in info:
                return 'Japan'
            if 'China' in info:
                return 'China'
            if 'South Korea' in info:
                return 'South Korea'
        except Exception:
            pass
    return 'Unknown'

def get_source_material(anime):
    source = anime.get('source')
    if source:
        return source
    # Try to scrape MyAnimeList page
    url = anime.get('url')
    if url:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            for span in soup.find_all('span', string='Source:'):
                return span.find_next('a').text.strip()
        except Exception:
            pass
    return 'Unknown'

def extract_fields(anime):
    # Get details
    details = get_anime_details(anime['mal_id'])
    # Fields
    image = details.get('images', {}).get('jpg', {}).get('large_image_url')
    name = details.get('title_english') or details.get('title')
    year = details.get('year')
    genres = [g['name'] for g in details.get('genres', [])]
    themes = [t['name'] for t in details.get('themes', [])]
    type_ = details.get('type')
    score = details.get('score')
    studios = [s['name'] for s in details.get('studios', [])]
    demographics = [d['name'] for d in details.get('demographics', [])]
    episodes = details.get('episodes')
    season = details.get('season')
    # Cross-referenced fields
    country = get_country_of_origin(details)
    source = get_source_material(details)
    # Compose
    return {
        'image': image,
        'name': name,
        'year': year,
        'genre': genres,
        'season': season,
        'type': type_,
        'score': score,
        'theme': themes,
        'studio': studios,
        'demographic': demographics,
        'country_of_origin': country,
        'source_material': source,
        'number_of_episodes': episodes
    }

def main():
    anime_list = []
    print(f'Fetching top {TOTAL} anime...')
    for page in tqdm(range(1, PAGES + 1)):
        try:
            top_anime = get_top_anime(page)
            for anime in top_anime:
                try:
                    data = extract_fields(anime)
                    anime_list.append(data)
                except Exception as e:
                    print(f"Error extracting anime {anime.get('title')}: {e}")
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(anime_list, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(anime_list)} anime to {OUTPUT_FILE}')

if __name__ == '__main__':
    main() 
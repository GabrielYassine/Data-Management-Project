import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

def fetch_pokemon_details(url):
    """Fetch details for a single Pokémon by its API URL."""
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return {"id": data["id"], "name": data["name"]}
    else:
        print(f"Something went wrong while fetching {url}")
        return None

def get_pokemon_parallel(amount):
    """Fetch Pokémon details in parallel."""
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={amount}')
    if r.status_code != 200:
        print(f"Something went wrong fetching list of Pokémon, error code: {r.status_code}")
        return []

    pokemon_data = r.json()
    urls = [pokemon["url"] for pokemon in pokemon_data["results"]]

    pokemon_info = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_pokemon_details, url): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                pokemon_info.append(result)

    # Sort by ID
    pokemon_info.sort(key=lambda x: x["id"])
    return pokemon_info

def save_to_json(data, filename="pokemon_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(data)} Pokémon to {filename}")

def load_from_json(filename="pokemon_data.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

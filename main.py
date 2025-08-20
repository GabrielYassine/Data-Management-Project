from API_gate import get_pokemon_parallel, save_to_json, load_from_json

def main():
    filename = "pokemon_data.json"
    force_fetch = False  # Set True to refresh cache

    if not force_fetch:
        cached_data = load_from_json(filename)
    else:
        cached_data = None

    if cached_data and len(cached_data) > 0:
        print(f"Loaded {len(cached_data)} Pokémon from cache")
        pokemon_info = cached_data
    else:
        print("Fetching fresh Pokémon data from API...")
        pokemon_info = get_pokemon_parallel(151)
        save_to_json(pokemon_info, filename)

    print("API data ready for use")

if __name__ == "__main__":
    main()

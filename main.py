import requests

r = requests.get('https://pokeapi.co/api/v2/pokemon/ditto/')
if r.status_code == 200:
    pokemon_data = r.json()
    pokemon_info = {
        "name": pokemon_data["name"]
    }
    print(pokemon_info)
import requests, json

def get_pokemon_data(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'name':pokemon.upper(),
            'id':data['id'],
            'poke_type':[t['type']['name'] for t in data['types']],
            'img':data['sprites']['front_default'],
            'weight':data['weight']/10,
            'height':data['height']/10,
            'stats':{f"base_{stat['stat']['name']}".replace("-","_") : stat['base_stat'] for stat in data['stats']}
        }
    
def get_pokemon_species(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # with open ('species.json', 'w') as f:
        #     json.dump(data, f, indent=4)
        if data['evolves_from_species']:
            return {
                'species_url':data['evolution_chain']['url'],
                'previous_stage': data['evolves_from_species']['name']
            }
        else:
            return {
                'species_url':data['evolution_chain']['url'],
                'previous_stage': None
            }

def get_pokemon_id_before_after(pokemon_id):
    ids = {'before': pokemon_id - 1, 'after': pokemon_id + 1}
    for key, val in ids.items():
        try:
            url = f'https://pokeapi.co/api/v2/pokemon-species/{val}'
            response = requests.get(url)
            data = response.json()
            if data['varieties']:
                ids[key] = data['varieties'][0]['pokemon']['name']
        except (requests.RequestException, KeyError, IndexError):
            ids[key] = None
        
    return ids

def get_pokemon_evolution(evolution_url, target_name):
    response = requests.get(evolution_url)
    if response.status_code == 200:
        data = response.json()
        return find_next_evolution(data['chain'], target_name.lower())
    return None

def find_next_evolution(chain, target_name):
    # Cek apakah node saat ini adalah Pokémon yang diinput user
    if chain['species']['name'] == target_name:
        return [evo['species']['name'].capitalize() for evo in chain['evolves_to']]

    # Kalau belum ketemu, cari di dalam evolves_to
    for evo in chain['evolves_to']:
        result = find_next_evolution(evo, target_name)
        if result:
            return result

    return None       
    

def main(pokemon_name):
    pokemon_data = get_pokemon_data(pokemon_name)
    if pokemon_data:
        pokemon_species = get_pokemon_species(pokemon_data['id'])
        pokemon_evolution = get_pokemon_evolution(pokemon_species['species_url'], pokemon_name)
        pokemon_id_before_after = get_pokemon_id_before_after(pokemon_data['id'])
        pokemon_previous_data_img, pokemon_evolution_data_img = {}, {}
        
        if pokemon_species['previous_stage']:
            pokemon_previous_data = get_pokemon_data(pokemon_species['previous_stage'])
            pokemon_previous_data_img[pokemon_species['previous_stage']] = pokemon_previous_data['img']
        
        if pokemon_evolution:
            for i in pokemon_evolution:
                pokemon_evolution_data = get_pokemon_data(i)
                if pokemon_evolution_data:
                    pokemon_evolution_data_img[i] = pokemon_evolution_data['img']
                else:
                    pass
        return pokemon_data, pokemon_id_before_after, pokemon_previous_data_img, pokemon_evolution_data_img
    else:
        return None, None, None, None
    
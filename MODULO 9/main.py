import requests
import time
from tqdm import tqdm

BASE_URL = "https://pokeapi.co/api/v2/"
cache = {}

def get_json(url):
    if url in cache:
        return cache[url]
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        cache[url] = data
        time.sleep(0.1)
        return data
    except requests.exceptions.RequestException:
        return None

def pokemon_tipo(tipo):
    data = get_json(f"{BASE_URL}type/{tipo}")
    return [p['pokemon']['name'] for p in data['pokemon']] if data else []

def especie_base(pokemon_name):
    poke_data = get_json(f"{BASE_URL}pokemon/{pokemon_name}")
    return poke_data['species']['name'] if poke_data else None

def cadena_evolutiva(pokemon_name):
    species_data = get_json(f"{BASE_URL}pokemon-species/{pokemon_name}")
    if not species_data:
        return []
    evo_chain = get_json(species_data['evolution_chain']['url'])
    chain = []
    def recorrer(node):
        chain.append(node['species']['name'])
        for evo in node['evolves_to']:
            recorrer(evo)
    recorrer(evo_chain['chain'])
    return chain

# Resultados
resultados = []

# Tipo fuego en Kanto
fuego_kanto = []
for name in pokemon_tipo("fire"):
    base = especie_base(name)
    poke_data = get_json(f"{BASE_URL}pokemon/{base}")
    if poke_data and poke_data['id'] <= 151:
        fuego_kanto.append(base)
resultados.append(f"🔥 Pokémon tipo fuego en Kanto: {len(set(fuego_kanto))} → {sorted(set(fuego_kanto))}")

# Agua con altura > 10
agua_altos = []
for name in pokemon_tipo("water"):
    base = especie_base(name)
    poke_data = get_json(f"{BASE_URL}pokemon/{base}")
    if poke_data and poke_data['height'] > 10:
        agua_altos.append(base)
resultados.append(f"💧 Pokémon tipo agua con altura > 10: {sorted(set(agua_altos))}")

# Cadena evolutiva Bulbasaur
resultados.append(f"🌱 Cadena evolutiva de Bulbasaur: {cadena_evolutiva('bulbasaur')}")

# Eléctricos sin evolución
electrico_sin_evo = []
for name in pokemon_tipo("electric"):
    base = especie_base(name)
    species_data = get_json(f"{BASE_URL}pokemon-species/{base}")
    if not species_data:
        continue
    evo_chain = get_json(species_data['evolution_chain']['url'])
    if species_data['evolves_from_species'] is None and len(evo_chain['chain']['evolves_to']) == 0:
        electrico_sin_evo.append(base)
resultados.append(f"⚡ Pokémon eléctricos sin evolución: {sorted(set(electrico_sin_evo))}")

# Mayor ataque en Johto
max_attack, poke_max_attack = 0, None
for i in tqdm(range(152, 252), desc="Buscando mayor ataque en Johto", leave=False):
    poke = get_json(f"{BASE_URL}pokemon/{i}")
    if not poke:
        continue
    attack = next(stat['base_stat'] for stat in poke['stats'] if stat['stat']['name'] == 'attack')
    if attack > max_attack:
        max_attack, poke_max_attack = attack, poke['name']
resultados.append(f"💪 Pokémon con mayor ataque en Johto: {poke_max_attack} ({max_attack})")

# Mayor velocidad no legendario
max_speed, poke_max_speed = 0, None
for i in tqdm(range(1, 1025), desc="Buscando más rápido no legendario", leave=False):
    poke = get_json(f"{BASE_URL}pokemon/{i}")
    if not poke:
        continue
    species_data = get_json(poke['species']['url'])
    if species_data and not species_data['is_legendary']:
        speed = next(stat['base_stat'] for stat in poke['stats'] if stat['stat']['name'] == 'speed')
        if speed > max_speed:
            max_speed, poke_max_speed = speed, poke['name']
resultados.append(f"⚡ Pokémon más rápido no legendario: {poke_max_speed} ({max_speed})")

# Hábitat más común en planta
habitats = {}
for name in pokemon_tipo("grass"):
    base = especie_base(name)
    species_data = get_json(f"{BASE_URL}pokemon-species/{base}")
    if species_data and species_data['habitat']:
        h = species_data['habitat']['name']
        habitats[h] = habitats.get(h, 0) + 1
habitat_comun = max(habitats, key=habitats.get)
resultados.append(f"🌿 Hábitat más común entre plantas: {habitat_comun}")

# Menor peso
min_weight, poke_min_weight = float("inf"), None
for i in tqdm(range(1, 1025), desc="Buscando menor peso", leave=False):
    poke = get_json(f"{BASE_URL}pokemon/{i}")
    if poke and poke['weight'] < min_weight:
        min_weight, poke_min_weight = poke['weight'], poke['name']
resultados.append(f"⚖️ Pokémon de menor peso: {poke_min_weight} ({min_weight})")

# Mostrar
print("\n" + "="*50)
print("RESULTADOS FINALES")
print("="*50)
for r in resultados:
    print(r)

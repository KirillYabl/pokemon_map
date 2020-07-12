import folium

from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    html = f"""
        <h4>{name}</h4><br>
        <code>lat: {lat}</code><br>
        <code>lon: {lon}</code>
        """

    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
        popup=html
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in pokemon_entities:
        pokemon_image_path = DEFAULT_IMAGE_URL
        if pokemon_entity.pokemon.image:
            pokemon_image_path = pokemon_entity.pokemon.image.path
        add_pokemon(folium_map=folium_map,
                    lat=pokemon_entity.lat,
                    lon=pokemon_entity.lon,
                    name=pokemon_entity.pokemon.title.encode('utf-8'),
                    image_url=pokemon_image_path)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_url = ''
        if pokemon.image:
            pokemon_url = pokemon.image.url
        pokemons_on_page.append(
            {
                'pokemon_id': pokemon.id,
                'img_url': pokemon_url,
                'title_ru': pokemon.title
            }
        )

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    evolutions = requested_pokemon.next_evolutions.all()

    next_evolution = {}
    if evolutions:
        evolution_pokemon = evolutions[0]
        evolution_pokemon_image_url = DEFAULT_IMAGE_URL
        if evolution_pokemon.image:
            evolution_pokemon_image_url = evolution_pokemon.image.url
        next_evolution.update({
            'title_ru': evolution_pokemon.title,
            'pokemon_id': evolution_pokemon.id,
            'img_url': evolution_pokemon_image_url
        })

    previous_evolution = {}
    if requested_pokemon.previous_evolution:
        requested_pokemon_previous_evolution_image_url = DEFAULT_IMAGE_URL
        if requested_pokemon.previous_evolution.image:
            requested_pokemon_previous_evolution_image_url = requested_pokemon.previous_evolution.image.url
        next_evolution.update({
            'title_ru': requested_pokemon.previous_evolution.title,
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': requested_pokemon_previous_evolution_image_url
        })

    element_type = []
    elements = requested_pokemon.element_type.all()
    if elements:
        for element in elements:
            strong_against = [weak_element.title for weak_element in element.strong_against.all()]
            element_type.append({
                'title': element.title,
                'img': element.image.url,
                'strong_against': strong_against
            })

    requested_pokemon_image_url = DEFAULT_IMAGE_URL
    if requested_pokemon.image:
        requested_pokemon_image_url = requested_pokemon.image.url
    pokemon_json = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.en_title,
        "title_jp": requested_pokemon.jp_title,
        "description": requested_pokemon.description,
        "img_url": requested_pokemon_image_url,
        "entities": [],
        "next_evolution": next_evolution,
        "previous_evolution": previous_evolution,
        "element_type": element_type
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    for pokemon_entity in pokemon_entities:
        entity = {
            "level": pokemon_entity.level,
            "lat": pokemon_entity.lat,
            "lon": pokemon_entity.lon
        }
        pokemon_json['entities'].append(entity)
        pokemon_image_path = DEFAULT_IMAGE_URL
        if requested_pokemon.image:
            pokemon_image_path = requested_pokemon.image.path
        add_pokemon(folium_map=folium_map,
                    lat=pokemon_entity.lat,
                    lon=pokemon_entity.lon,
                    name=requested_pokemon.title,
                    image_url=pokemon_image_path)
    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_json})

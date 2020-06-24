from django.contrib import admin
from .models import Pokemon, PokemonEntity, PokemonElementType


class ElementTypeInline(admin.TabularInline):
    model = Pokemon.element_type.through
    extra = 0


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    inlines = [
        ElementTypeInline,
    ]
    exclude = ('element_type',)
    list_filter = ('element_type',)


@admin.register(PokemonElementType)
class PokemonElementTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ('strong_against',)
    list_filter = ('strong_against',)


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'lat', 'lon', 'appeared_at', 'disappeared_at', 'level')
    list_filter = ('pokemon', 'level')

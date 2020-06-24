from django.contrib import admin
from .models import Pokemon, PokemonEntity, PokemonElementType


class ElementTypeInline(admin.TabularInline):
    model = Pokemon.element_type.through
    extra = 0


class PokemonAdmin(admin.ModelAdmin):
    inlines = [
        ElementTypeInline,
    ]
    exclude = ('element_type',)


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity)
admin.site.register(PokemonElementType)

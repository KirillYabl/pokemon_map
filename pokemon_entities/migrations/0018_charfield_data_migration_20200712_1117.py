from django.db import migrations, models


def from_none_to_default(apps, schema_editor):
    Pokemon = apps.get_model('pokemon_entities', 'Pokemon')
    for pokemon in Pokemon.objects.all():
        if pokemon.description is None:
            pokemon.description = ''
        if pokemon.en_title is None:
            pokemon.en_title = ''
        if pokemon.jp_title is None:
            pokemon.jp_title = ''
        pokemon.save()


class Migration(migrations.Migration):
    dependencies = [
        ('pokemon_entities', '0017_auto_20200712_1109'),
    ]

    operations = [
        migrations.RunPython(from_none_to_default),
    ]

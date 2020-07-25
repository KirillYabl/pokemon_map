from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField(verbose_name='название стихии', max_length=200)
    image = models.ImageField(verbose_name='картинка', null=True)
    strong_against = models.ManyToManyField(
        verbose_name='силен против',
        to='self',
        blank=True,
        symmetrical=False,
        related_name='weaknesses'
    )

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    title = models.CharField(verbose_name='имя', max_length=200)
    image = models.ImageField(verbose_name='картинка', null=True, blank=True)
    description = models.TextField(verbose_name='описание', blank=True)
    en_title = models.CharField(verbose_name='имя на английском', max_length=200, blank=True)
    jp_title = models.CharField(verbose_name='имя на японском', max_length=200, blank=True)
    previous_evolution = models.ForeignKey(
        verbose_name='предыдущая эволюция',
        to='self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions'
    )
    element_type = models.ManyToManyField(
        verbose_name='стихии покемона',
        to=PokemonElementType,
        blank=True,
        related_name='pokemons'
    )

    def __str__(self):
        elements = [str(element) for element in self.element_type.all()]
        return f'{self.title}. Стихии: "{", ".join(elements)}"'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(to=Pokemon, verbose_name='покемон', on_delete=models.CASCADE, related_name='entities')
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='появится', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='исчезнет', null=True, blank=True)
    level = models.IntegerField(verbose_name='уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='сила', null=True, blank=True)
    defense = models.IntegerField(verbose_name='защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title}: {self.lat}, {self.lon}'

from django.db import models

# Create your models here.


class Pokemons(models.Model):
    """
    Users data
    """
    user_name = models.TextField("Username")
    pokemons_names = models.TextField("pokemons")

    def __str__(self) -> str:
        return self.user_name

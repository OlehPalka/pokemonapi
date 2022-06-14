from rest_framework.serializers import ModelSerializer
from .models import Pokemons


class PokemonDataSerializer(ModelSerializer):

    class Meta:
        model = Pokemons
        fields = '__all__'

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import requests

from pokeapi_main.models import Pokemons


class RegUserForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Password'
        self.fields['password2'].label = 'Confirm_password'

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("This name is already taken!")

        return username

    def clean(self):
        cleaned_data = super(RegUserForm, self).clean()

        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password2")
        if password != password_2:
            raise forms.ValidationError("Passwords are not coincedent!")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class LoginUserForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Incorrect user name!")
        return username

    def clean(self):
        cleaned_data = super(LoginUserForm, self).clean()
        user_name = cleaned_data.get("username")
        user_pass = cleaned_data.get("password")

        user = User.objects.filter(username=user_name).first()
        if user is not None:
            if not user.check_password(user_pass):
                raise forms.ValidationError("Incorrect password")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class FindPokemonForm(ModelForm):

    pokemon = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Pokemon name"
    }))

    request_url = "https://pokeapi.co/api/v2/pokemon/"

    def set_request_url(self, url):
        """
        Url should take pokemon name as the last symbols
        """
        self.request_url = url

    def pokemon_data(self, pokemon_name):
        """
        This function gets information about pokemon (dict).
        """
        base_url = self.request_url + pokemon_name.lower()
        data = requests.get(base_url).json()
        poke_abilities = [ability['ability']['name'].capitalize()
                          for ability in data['abilities']]
        poke_abilities = ", ".join(poke_abilities)
        return pokemon_name, poke_abilities

    def clean_pokemon(self):
        """
        Checks wether such pokemon exists or not.
        """
        try:
            pokemon, poke_abilities = self.pokemon_data(
                self.cleaned_data["pokemon"])
        except Exception:
            raise forms.ValidationError("There is no such pokemon.")

        return pokemon, poke_abilities

    class Meta:
        model = Pokemons
        fields = ["pokemon"]

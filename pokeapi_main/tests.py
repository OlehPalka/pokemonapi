from django.test import TestCase

# Create your tests here.
import unittest
from unittest import mock
from django.urls import reverse
from .forms import RegUserForm, FindPokemonForm


class RegistrationTest(unittest.TestCase):

    def test_reg_form_with_data(self):
        form = RegUserForm(data={
            'username': 'TestUser',
            'email': 'testuser@gmail.com',
            'password': '1234',
            'password2': '1234'
        })

        self.assertTrue(form.is_valid())

    def test_reg_form_without_data(self):
        form = RegUserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)


class SelectPokemonTest(unittest.TestCase):

    @mock.patch('pokeapi_main.forms.FindPokemonForm.pokemon_data', return_value=('ditto', 'Limber, Imposter, Test'))
    def test_find_pokemon_form_with_correct_data(self, mock_output):

        form = FindPokemonForm(data={'pokemon': 'ditto'})
        self.assertTrue(form.is_valid())

    @mock.patch('pokeapi_main.forms.FindPokemonForm.pokemon_data', return_value=Exception())
    def test_find_pokemon_form_with_incorrect_data(self, mock_output):

        form = FindPokemonForm(data={'pokemon': 'paket'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_find_pokemon_form_without_data(self):

        form = FindPokemonForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

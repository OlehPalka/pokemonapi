from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.views import View

from pokeapi_main.serializer import PokemonDataSerializer
from .forms import *
from .models import Pokemons
from .serializer import PokemonDataSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.


class RegUserView(CreateView):

    def get(self, request, *args, **kwargs):
        form = RegUserForm(request.POST or None)
        context = {'form': form}
        return render(request, "pokeapi_main/register.html", context)

    def post(self, request, *args, **kwargs):
        form = RegUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data["username"]
            new_user.email = form.cleaned_data["email"]
            new_user.save()
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, "pokeapi_main/register.html", context)


class LoginUserView(LoginView):

    def get(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST or None)
        context = {'form': form}
        return render(request, "pokeapi_main/login.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST or None)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, "pokeapi_main/login.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


class IndexView(View):

    def get(self, request, *args, **kwargs):
        form = FindPokemonForm(request.POST or None)

        if request.user.is_authenticated:
            user_name = request.user.username

            if Pokemons.objects.filter(user_name=user_name).exists():
                user = Pokemons.objects.get(user_name=user_name)
                pokemons_list = eval(user.pokemons_names)
                context = {"pokemons": pokemons_list, 'form': form}
                return render(request, "pokeapi_main/index.html", context)

        context = {'form': form}
        return render(request, "pokeapi_main/index.html", context)

    def post(self, request, *args, **kwargs):

        form = FindPokemonForm(request.POST or None)
        if form:

            if form.is_valid():

                if request.user.is_authenticated:

                    user_name = request.user.username
                    if not Pokemons.objects.filter(user_name=user_name).exists():
                        new_user = form.save(commit=False)
                        new_user.user_name = user_name
                        new_user.pokemons_names = str(
                            [form.cleaned_data["pokemon"][0].capitalize()])
                        new_user.save()
                    else:
                        user = Pokemons.objects.get(user_name=user_name)
                        pokemons_list = eval(user.pokemons_names)
                        if form.cleaned_data["pokemon"][0].capitalize() not in pokemons_list:
                            if len(pokemons_list) >= 10:
                                for _ in range(len(pokemons_list) - 9):
                                    del pokemons_list[0]
                            pokemons_list.append(
                                form.cleaned_data["pokemon"][0].capitalize())
                            user.pokemons_names = str(pokemons_list)
                            user.save()
                context = {
                    "pokemon": form.cleaned_data["pokemon"][0].capitalize(), "pokemon_desc":  form.cleaned_data["pokemon"][1]}
                request.session['one'] = context
                return HttpResponseRedirect("/description")

            context = {"form": form}
            if request.user.is_authenticated:
                user_name = request.user.username
                user = Pokemons.objects.get(user_name=user_name)
                pokemons_list = eval(user.pokemons_names)
                context = {"pokemons": pokemons_list, 'form': form}

            return render(request, "pokeapi_main/index.html", context)


def description(request):
    """
    Loads description page.
    """
    context = request.session['one']
    return render(request, "pokeapi_main/description.html", context)


class CheckDataApi(ModelViewSet):
    """
    Api class
    """

    queryset = Pokemons.objects.all()
    serializer_class = PokemonDataSerializer

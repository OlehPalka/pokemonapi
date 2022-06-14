from django.urls import path
from django.views.generic.base import View
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="pokeapi_main"),
    path('register', views.RegUserView.as_view(), name='register'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('description', views.description)
]

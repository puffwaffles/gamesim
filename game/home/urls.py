from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('tutorial/', views.tutorial, name = "tutorial"),
    path('account', views.promptaccount, name = "promptaccount"),
    path('login', views.login, name = "login"),
    path('signup', views.signup, name = "signup"),
    path('homescreen/', views.actualhome, name = "actualhome"),
    path('loadsaves/', views.loadsaves, name = "loadsaves"),
    path('createsave/', views.createsave, name = "createsave"),
    path('deletesave/', views.deletesave, name = "deletesave"),
    path('gamehome/', views.gamehome, name = "gamehome"),
    path('inventory/', views.displayinventory, name = "displayinventory"),
    path('shop/', views.shop, name = "shop"),
    path('summon/', views.summon, name = "summon"),
    path('summonresults/', views.summonresults, name = "summonresults"),
    path('roster/', views.roster, name = "roster"),
]
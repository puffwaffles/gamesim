from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('tutorial/', views.tutorial, name = "tutorial"),
    path('homescreen/', views.actualhome, name = "actualhome"),
    path('loadsaves/', views.loadsaves, name = "loadsaves"),
    path('createsave/', views.createsave, name = "createsave"),
    path('deletesave/', views.deletesave, name = "deletesave"),
    path('loadtemp/', views.inittemp, name = "inittemp"),
    path('savetemp/', views.savetemp, name = "savetemp"),
    path('changeamount/', views.changeamount, name = "changeamount"),
    path('gamehome/', views.gamehome, name = "gamehome"),
    path('inventory/', views.displayinventory, name = "displayinventory"),
    path('release/', views.releasecharacter, name = "releasecharacter"),
    path('shop/', views.shop, name = "shop"),
]
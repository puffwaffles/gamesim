from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('loadsaves/', views.loadsaves, name = "loadsaves"),
    path('createsave/', views.createsave, name = "createsave"),
    path('deletesave/', views.deletesave, name = "deletesave"),
    path('inittemp/', views.inittemp, name = "inittemp"),
    path('savetemp/', views.savetemp, name = "savetemp"),
    path('changeamount/', views.changeamount, name = "changeamount"),
    path('gamehome/', views.gamehome, name = "gamehome"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name = "home"),
    path('loadsaves/', views.loadsaves, name = "loadsaves"),
    path('createsave/', views.createsave, name = "createsave"),

]
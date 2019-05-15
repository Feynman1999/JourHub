from django.urls import include,path
from .views import *

urlpatterns = [
    path('login/',login),
    path('register/',register),
    path('<int:id>/',profile),
]
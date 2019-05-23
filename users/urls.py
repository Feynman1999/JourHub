from django.urls import include,path
from .views import *

urlpatterns = [
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('password/',password,name='password'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('profile/change/',change,name='change')
]
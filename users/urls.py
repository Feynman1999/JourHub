from django.urls import include,path
from .views import *

urlpatterns = [
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout,name='logout'),
    path('<int:id>/',profile),
    path('<int:id>/change/',change)
]
from django.urls import include,path
from .views import *

urlpatterns = [
    path('<int:id>/',get_periodical),
    path('paper/<int:id>',get_paper),
    path('<name>/',get_periodicals),
]
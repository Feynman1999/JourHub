from django.urls import include,path
from .views import *

urlpatterns = [
    path('periodical=<name>/',get_periodicals),
    path('pappers=<name>/',get_papers),
    path('<int:id>/',get_periodical),
    path('papper/<int:id>/',get_paper),
    path('borrow=<int:id>+<int:day>/',borrow),
    path('add/',add,name='add'),
    
]
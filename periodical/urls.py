from django.urls import include,path
from .views import *

urlpatterns = [
    # 期刊名
    path('periodical=<name>/',get_periodicals),
    path('search/',search),
    path('<int:id>/',get_periodical),
    path('papper/<int:id>/',get_paper),
    path('borrow=<int:id>+<int:day>/',borrow),
    path('borrowlist/',borrowlist),
    path('add/',add,name='add'),
    path('addlist/',addlist,name='addlist'),
]
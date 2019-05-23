from django.urls import include,path
from .views import *

urlpatterns = [
    # 导航栏
    path('barperiodical/',barperiodical,name='barperiodical'),
    # 查看期刊名对应有哪些卷期
    path('periodical=<name>/',get_periodicals,name='periodical'),
    # 搜索期刊或者论文
    path('search/',search,name = 'search'),
    # 查看具体哪一期
    path('<int:id>/',get_periodical),
    # 查看具体哪一篇论文
    path('paper/<int:id>/',get_paper),
    # 借期刊
    path('borrow=<int:id>+<int:day>/',borrow),
    # 查看借书记录
    path('borrowlist/',borrowlist,name='borrowlist'),
    # 还期刊
    path('return/<int:id>',returnPeriod),
    
    # 征订列表
    path('addlist/',addlist,name='addlist'),
    # 管理员征订
    path('add/',add,name='add'),
    # 管理员登记
    path('checkin/<int:id>/',checkin,name='checkin'),
]
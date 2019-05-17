from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from periodical import models
# 访问具体哪一个期刊的第几期
def get_periodical(request,id):
    periodical = list(models.Periodical.objects.filter(id = id))
    pappers = list(models.Paper.objects.filter(Belong_id = id))
    context={}
    context['periodical']=periodical[0]
    context['pappers']=pappers
    return render(request,'periodical.html',context)

# 访问哪一个期刊
def get_periodicals(request,name):
    periodicals = list(models.Periodical.objects.filter(Name = name))
    context={}
    context['result'] = periodicals
    return render(request,'search.html',context)

def get_papers(request,name):
    pappers = list(models.Paper.objects.filter(Title = name))
    context={}
    context['result'] = pappers
    return render(request,'search.html',context)

# 访问具体文章
def get_paper(request,id):
    papper = list(models.Paper.objects.filter(id = id))
    context={}
    context['papper']=papper[0]
    return render(request,'papper.html',context)

# 征订新期刊
def add(request):
    if request.method == 'POST':
        pass
    pass

# 借阅期刊
def borrow(request,id,day):
    from django.contrib import auth
    res = list(auth.models.User.objects.filter(username=request.user).values('id'))
    user_id = res[0]['id']
    models.Borrow.objects.create(Person_id=user_id,Period_id=id,Borrow_Duration=day)
    return redirect('/periodical/%s' %(id,))

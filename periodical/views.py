from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from periodical import models
# 访问具体哪一个期刊的第几期
def get_periodical(request,id):
    periodical = list(models.Periodical.objects.filter(id = id))
    papers = list(models.Paper.objects.filter(Belong_id = id))
    context={}
    context['periodical']=periodical[0]
    context['papers']=papers
    return render(request,'periodical.html',context)

# 查找期刊或者论文
def search(request):
    if request.method == 'POST':
        context = {}
        SearchType = request.POST.get('type')
        Context = request.POST.get('context')
        if SearchType == 'periodical':
            result = list(models.Periodical.objects.filter(Name__contains = Context).distinct().order_by('Name'))
        elif SearchType == 'paper':
            result = list(models.Paper.objects.filter(Title__contains = Context))
        print(result)
        context['result'] = result
        context['type'] = SearchType
        context['context'] = Context
        return render(request,'search.html',context)

# 访问哪一个期刊
def get_periodicals(request,name):
    periodicals = list(models.Periodical.objects.filter(Name = name))
    context={}
    context['result'] = periodicals
    return render(request,'periodicals.html',context)


# 访问具体文章
def get_paper(request,id):
    paper = list(models.Paper.objects.filter(id = id))
    context={}
    context['paper']=paper[0]
    return render(request,'paper.html',context)

# 征订新期刊
def add(request):
    if request.method == 'POST':
        pass
    pass

def addlist(request):
    pass

# 借阅期刊
def borrow(request,id,day):
    from django.contrib import auth
    res = list(auth.models.User.objects.filter(username=request.user).values('id'))
    user_id = res[0]['id']
    models.Borrow.objects.create(Person_id=user_id,Period_id=id,Borrow_Duration=day,Borrow_Time=timezone.now())
    tmpPeriod = models.Periodical.objects.get(id=id)
    tmpPeriod.Reserve -= 1
    tmpPeriod.save()

    return redirect('/periodical/%s' %(id,))

def borrowlist(request):
    from django.contrib import auth
    res = list(auth.models.User.objects.filter(username=request.user))
    is_staff = res[0].is_staff
    # 管理员查看全部信息
    if is_staff == True:
        message = "Dear staff,welcome to this page"
        username = None
        if not request.POST.get('username'):
            username = request.POST.get('username')
            user_id = auth.models.User.objects.filter(username=username)
        if username == None:
            borrow_all = list(models.Borrow.objects.all().order_by('-id'))
        else:
            borrow_all = list(models.Borrow.objects.filter(Person_id=user_id).order_by('-id'))
        
    # 用户只能查看自己的
    else:
        message = "Dear user , welcome to this page"
        user_id = res[0]['id']
        borrow_all = list(models.Borrow.objects.filter(Person_id=user_id).order_by('-id'))
    

    # 需要把每个借阅记录的用户名和期刊名得到，并放入一个list
    result = []
    for it in borrow_all:
        tmpUsr = list(auth.models.User.objects.filter(id=it.Person_id))
        tmpPeriod = list(models.Periodical.objects.filter(id=it.Period_id))
        tmpDict ={}
        tmpDict['user'] = tmpUsr[0];tmpDict['period'] = tmpPeriod[0]
        tmpDict['borrow'] = it
        result.append(tmpDict)

    context = {}
    context['message'] = message
    context['result'] = result
    return render(request,'borrowlist.html',context)

def returnPeriod(request,id):
    # 判断是否有还书的权限
    from django.contrib import auth
    who = list(auth.models.User.objects.filter(username=request.user).values('id'))
    who_id = who[0]['id']
    borrow = list(models.Borrow.objects.filter(id=id))
    borrow = borrow[0]
    if who_id != borrow.Person_id:
        return render(request,'error.html',{'message':'不能还不是自己借阅的期刊'})

    # bug 时间不能update
    borrow.Return_Time = timezone.now()
    borrow.Return = True
    borrow.save()
    print('borrow.ReturnTime=',borrow.Return_Time)

    # 库存数量加一
    Period_id = borrow.Period_id
    tmpPeriod = models.Periodical.objects.get(id=Period_id)
    tmpPeriod.Reserve = tmpPeriod.Reserve
    tmpPeriod.save()
    return redirect('/periodical/borrowlist')

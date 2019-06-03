from django.shortcuts import render, redirect, reverse
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from periodical import models
from django.contrib import auth

# 导航栏
def barperiodical(request):
    context = {}
    periodicals = models.Periodical.objects.filter(Status=True).values('Name').distinct().order_by('Name')
    context['periodicals'] = periodicals
    return render(request,'periodical/barperiodical.html',context)

# 访问具体哪一个期刊的第几期
def get_periodical(request,id):
    periodical = models.Periodical.objects.get(id = id)
    papers = list(models.Paper.objects.filter(Belong_id = id))
    context={}
    context['periodical']=periodical
    context['papers']=papers
    return render(request,'periodical/periodical.html',context)

# 查找期刊或者论文
def search(request):
    if request.method == 'POST':
        context = {}
        SearchType = request.POST.get('type')
        Context = request.POST.get('context')
        Level = request.POST.get('level')
        if Level == 'False':
            if SearchType == 'periodical':
                result = models.Periodical.objects.filter(Name__contains = Context).distinct().order_by('Name')
            elif SearchType == 'paper':
                # 也搜索关键字
                res1 = models.Paper.objects.filter(Title__contains = Context)
                res2 = models.Paper.objects.filter(KeyWords__contains = Context)
                result = res1 | res2
        # 进行高级搜索
        else:
            
            # print(Level)
            # print(type(Year),type(Volume),type(Phase))
            # print(Year,Volume,Phase)
            if SearchType == 'periodical':
                Year = request.POST.get('Year')
                Volume = request.POST.get('Volume')
                Phase = request.POST.get('Phase')
                result = models.Periodical.objects.filter(Name__contains = Context,
                Year__contains=Year,Volume__contains=Volume,
                Phase__contains=Phase).distinct().order_by('Name')
                context['level'] = {'Year':Year,'Volume':Volume,'Phase':Phase}
            elif SearchType == 'paper':
                Auther = request.POST.get('Auther')
                Pages_Start = request.POST.get('Pages_Start')
                Pages_End = request.POST.get('Pages_End')
                # 也搜索关键字
                # >=start
                if Pages_Start == "" and Pages_End == "":
                    res1 = models.Paper.objects.filter(Title__contains = Context,Auther__contains=Auther)
                    res2 = models.Paper.objects.filter(KeyWords__contains = Context,Auther__contains=Auther)    
                elif Pages_End == "":
                    res1 = models.Paper.objects.filter(Title__contains = Context,
                Auther__contains=Auther,Pages_Start__gte=Pages_Start)
                    res2 = models.Paper.objects.filter(KeyWords__contains = Context,
                Auther__contains=Auther,Pages_Start__gte=Pages_Start)    
                # <=end
                elif Pages_Start == "":
                    res1 = models.Paper.objects.filter(Title__contains = Context,
                Auther__contains=Auther,Pages_End__lte=Pages_End)
                    res2 = models.Paper.objects.filter(KeyWords__contains = Context,
                Auther__contains=Auther,Pages_End__lte=Pages_End)   
                # >=start  <=end
                else:
                    res1 = models.Paper.objects.filter(Title__contains = Context,
                Auther__contains=Auther,Pages_Start__gte=Pages_Start,
                Pages_End__lte=Pages_End)
                    res2 = models.Paper.objects.filter(KeyWords__contains = Context,
                Auther__contains=Auther,Pages_Start__gte=Pages_Start,
                Pages_End__lte=Pages_End)
                result = res1 | res2
                result.distinct()
                context['level'] = {'Auther':Auther,'Pages_Start':Pages_Start,'Pages_End':Pages_End}
        context['result'] = result
        context['type'] = SearchType
        context['context'] = Context
        return render(request,'periodical/search.html',context)
    return redirect('/')

# 访问哪一个期刊
def get_periodicals(request,name):
    periodicals = models.Periodical.objects.filter(Name = name,Status=True).order_by('-id')
    context={}
    periodList = list(periodicals)
    if len(periodList) != 0:
        context['basic'] = periodList[0]
    context['result'] = periodicals
    return render(request,'periodical/periodicals.html',context)


# 访问具体文章
def get_paper(request,id):
    paper = models.Paper.objects.get(id = id)
    periodical = models.Periodical.objects.get(id = paper.Belong_id)
    context={}
    context['paper'] = paper
    context['periodical'] = periodical
    return render(request,'periodical/paper.html',context)

# 征订新期刊
def add(request):
    # 权限控制
    if request.user.is_staff == False:
        return redirect('/')
    if request.method == 'POST':
        errors = []
        Name = request.POST.get('Name')
        Year = request.POST.get('Year')
        Number = request.POST.get('Number')
        Phase = request.POST.get('Phase')
        Cycle = request.POST.get('Cycle')
        Postal = request.POST.get('Postal')
        CN = request.POST.get('CN')
        ISSN = request.POST.get('ISSN')
        Locus = request.POST.get('Locus')
        Total = request.POST.get('Total')

        if Name == "":
            errors.append('请填写期刊名称')
        if Year == "":
            errors.append('请填写期刊年份')
        if Number == "":
            errors.append('请填写订阅期数')
        if Phase == "":
            errors.append('请填写期刊开始期号')
        if Cycle == "":
            errors.append('请填写期刊发布周期')
        if Postal == "":
            errors.append('请填写邮政编码')
        if CN == "":
            errors.append('请填写CN号')
        if ISSN == "":
            errors.append('请填写ISSN号')
        if Locus == "":
            errors.append('请填写所在地')
        if Total == "":
            errors.append('请填写订阅总数')
        # 填写信息不出错
        if len(errors) == 0:
            Number_Phase = 365 // int(Cycle)
            for it in range(int(Number)):
                # 跨年的时候的时间判断
                now_Year = int(Year) + (int(Phase) + it) // (Number_Phase+1)
                now_Phase = (int(Phase) + it) % Number_Phase
                if now_Phase == 0:
                    now_Phase = Number_Phase
                models.Periodical.objects.create(Name=Name,Year=str(now_Year),
                Phase=str(now_Phase),Cycle=Cycle,Postal=Postal,
                CN=CN,ISSN=ISSN,Locus=Locus,Reserve=Total,Total=Total,
                Status=False,Order_Time=timezone.now(),Responsibler_id=request.user.id)
            
            return redirect('/periodical/addlist')
        else:
            context = {}
            context['message'] = errors
            context['Name'] = Name
            context['Phase'] = Phase
            context['Postal'] = Postal
            context['Cycle'] = Cycle
            context['CN'] = CN
            context['ISSN'] = ISSN
            context['Locus'] = Locus
            context['Total'] = Total
            return render(request,'periodical/add.html',context)
    else:
        Name = request.GET.get('name')
        if Name != None:            
            periodicals = models.Periodical.objects.filter(Name=Name).order_by('-id')[:6]
            TmpList = list(periodicals)
            if len(TmpList) == 0:
                return redirect('/')
            context = {}
            context['Name'] = TmpList[0].Name
            context['Postal'] = TmpList[0].Postal
            context['Cycle'] = TmpList[0].Cycle
            context['CN'] = TmpList[0].CN
            context['ISSN'] = TmpList[0].ISSN
            context['Locus'] = TmpList[0].Locus
            context['Periodicals'] = periodicals
            return render(request,'periodical/add.html',context)
        else:
            return render(request,'periodical/add.html')
    return render(request,'periodical/add.html')

# 征订列表
def addlist(request):
    # 权限控制
    if request.user.is_staff == False:
        return redirect('/')
    context={}
    context['checked'] = models.Periodical.objects.filter(Status=True).order_by('-id')
    context['notcheck'] = models.Periodical.objects.filter(Status=False).order_by('-id')
    return render(request,'periodical/addlist.html',context)
    
# 到货之后登记信息
def checkin(request,id):
    # 权限控制
    if request.user.is_staff == False:
        return redirect('/')
    context = {}

    # local page post
    if request.method == 'POST':
        errors = []
        papers = []
        tmpPeriod = models.Periodical.objects.get(id=id)
        Volume = request.POST.get('Volume')
        if Volume == "":
            errors.append('请输入卷号')
            
        number = tmpPeriod.PaperNumber
        for i in range(number):
            paper = {}
            Title = request.POST.get('Title_%d'%(i+1,))
            Auther = request.POST.get('Auther_%d'%(i+1,))
            KeyWords = request.POST.get('KeyWords_%d'%(i+1,))
            Pages_Start = request.POST.get('Pages_Start_%d'%(i+1,))
            Pages_End = request.POST.get('Pages_End_%d'%(i+1,))
            Abstract = request.POST.get('Abstract_%d'%(i+1,))
            if Title == "":
                errors.append('请输入第%d篇论文的标题'%(i+1,))
            if Auther == "":
                errors.append('请输入第%d篇论文的作者'%(i+1,))
            if KeyWords == "":
                errors.append('请输入第%d篇论文的关键词'%(i+1,))
            if Pages_Start == "":
                errors.append('请输入第%d篇论文的开始页码'%(i+1,))
            if Pages_End == "":
                errors.append('请输入第%d篇论文的结束页码'%(i+1,))
            if Abstract.strip() == "":
                errors.append('请输入第%d篇论文的摘要'%(i+1,))

            # 为了能在出错的时候把数据还原，不管是否存在，都放进字典
            paper['Title'] = Title
            paper['Auther'] = Auther
            paper['KeyWords'] = KeyWords
            paper['Pages_Start'] = Pages_Start
            paper['Pages_End'] = Pages_End
            paper['Abstract'] = Abstract.strip()
            papers.append(paper)
        # 内容验证成功
        if len(errors) == 0:
            tmpPeriod = models.Periodical.objects.get(id=id)
            tmpPeriod.Status = True
            tmpPeriod.Volume = Volume
            tmpPeriod.save()
            for it in papers:
                models.Paper.objects.create(Title=it['Title'],Auther=it['Auther'],
                    KeyWords=it['KeyWords'],
                    Pages_Start=it['Pages_Start'],
                    Pages_End=it['Pages_End'],
                    Abstract=it['Abstract'],Belong_id=id)
            return redirect('/periodical/addlist/')
        # 内容验证失败
        else:
            tmpList = []
            for i in range(number):
                tmpList.append(i+1)
            context['Volume'] = Volume
            context['number'] = tmpList
            context['periodical']=models.Periodical.objects.get(id=id)        
            context['values'] = papers
            context['message'] = errors
            return render(request,'periodical/checkin.html',context)
    else:
        # addlist jump to here
        number = request.GET.get('number')
        if number == None:
            number = 3
        else:
            number = int(number)
        tmpList = []
        for i in range(number):
            tmpList.append(i+1)
        context['number'] = tmpList
        tmpPeriod = models.Periodical.objects.get(id=id)
        tmpPeriod.PaperNumber = number
        tmpPeriod.save()
        context['periodical']=models.Periodical.objects.get(id=id)
        return render(request,'periodical/checkin.html',context)
    

# 借阅期刊
def borrow(request,id,day):
    if request.user.is_authenticated == False:
        return redirect('/')
    res = auth.models.User.objects.get(username=request.user)
    models.Borrow.objects.create(Person_id=res.id,Period_id=id,Borrow_Duration=day,Borrow_Time=timezone.now())
    tmpPeriod = models.Periodical.objects.get(id=id)
    tmpPeriod.Reserve -= 1
    tmpPeriod.Borrow_Count += 1
    tmpPeriod.save()

    return redirect('/periodical/%s' %(id,))

def borrowlist(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    res = auth.models.User.objects.get(username=request.user)
    is_staff = res.is_staff
    context = {}
    # 管理员查看全部信息
    if is_staff == True:
        message = "亲爱的管理员，欢迎来到本页面，您可以搜索所有用户的借阅信息"
        username = None
        # 查询某个人或者某个期刊的借阅情况
        if request.method == 'POST':
            SearchType = request.POST.get('type')
            Context = request.POST.get('context')
            context['TYPE'] = SearchType
            context['CONTEXT'] = Context
            from itertools import chain
            # 搜索某一用户
            if SearchType == 'user':
                users = auth.models.User.objects.filter(username__contains=Context)
                # users is queryset
                tmpborrow = []
                for it in users:
                    tmpborrow.append(models.Borrow.objects.filter
                    (Person_id=it.id).order_by('-id'))
                if len(tmpborrow) == 0:
                    borrow_all = models.Borrow.objects.none()
                else:
                    borrow_all = tmpborrow[0]
                    for i in range(len(tmpborrow)):
                        if i == 0:
                            continue
                        borrow_all = borrow_all | tmpborrow[i]
                
            # 搜索某一期刊
            else:
                periodicals = models.Periodical.objects.filter(Name__contains=Context)
                tmpborrow = []
                for it in periodicals:
                    tmpborrow.append(models.Borrow.objects.filter(Period_id=it.id).order_by('-id'))
                if len(tmpborrow) == 0:
                    borrow_all = models.Borrow.objects.none()
                    
                else:
                    borrow_all = tmpborrow[0]
                    for i in range(len(tmpborrow)):
                        if i == 0:
                            continue
                        borrow_all = borrow_all | tmpborrow[i]
            
        else:
            borrow_all = models.Borrow.objects.all().order_by('-id')
            
        
    # 用户只能查看自己的
    else:
        message = "亲爱的用户，欢迎来到本页面"
        user_id = res.id
        borrow_all = models.Borrow.objects.filter(Person_id=user_id).order_by('-id')
    

    # 需要把每个借阅记录的用户名和期刊名得到，并放入一个list
    result = []
    for it in borrow_all:
        tmpDict ={}
        tmpDict['user'] = auth.models.User.objects.get(id=it.Person_id)
        tmpDict['period'] = models.Periodical.objects.get(id=it.Period_id)
        tmpDict['borrow'] = it
        tmpDict['id'] = it.id
        result.append(tmpDict)

    
    context['message'] = message
    context['result'] = result
    return render(request,'periodical/borrowlist.html',context)

def returnPeriod(request,id):
    # 判断是否有还书的权限
    who = auth.models.User.objects.get(username=request.user)
    borrow = models.Borrow.objects.get(id=id)
    if who.id != borrow.Person_id and who.is_staff == False:
        return render(request,'error.html',{'message':'不能还不是自己借阅的期刊'})

    borrow.Return_Time = timezone.now()
    borrow.Return = True
    borrow.save()

    # 库存数量加一
    Period_id = borrow.Period_id
    tmpPeriod = models.Periodical.objects.get(id=Period_id)
    tmpPeriod.Reserve += 1
    tmpPeriod.save()
    return redirect('/periodical/borrowlist')

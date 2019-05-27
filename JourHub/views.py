from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from periodical import models

# 主页
def index(request):
    context = {}
    context['periodicals'] = models.Periodical.objects.filter(Status=True).order_by('-Borrow_Count')[:5]
    queryList = models.Borrow.objects.all().order_by('-id')[:6]
    tmpList = []
    for it in queryList:
        tmpDict = {}
        tmpPeriod = models.Periodical.objects.get(id=it.Period_id)
        tmpDict['period'] = tmpPeriod
        tmpDict['borrow'] = it
        tmpList.append(tmpDict)
    context['borrow'] = tmpList
    return render(request,'index.html',context)

# 其他
def about(request):
    return render(request,'about.html')
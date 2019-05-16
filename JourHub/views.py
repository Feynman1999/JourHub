from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse

# 主页
def index(request):
    from periodical import models
    context = {}
    context['periodicals'] = list(models.Periodical.objects.all())
    return render(request,'index.html',context)

# 其他
def about(request):
    return render(request,'about.html')
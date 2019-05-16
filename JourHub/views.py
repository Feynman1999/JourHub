from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse

# 主页
def index(request):
    return render(request,'index.html')

# 其他
def about(request):
    return render(request,'about.html')
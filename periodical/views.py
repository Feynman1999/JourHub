from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
# 访问具体哪一个期刊的第几期
def get_periodical(request,id):
    return HttpResponse('now id is %d' % (id))

# 访问哪一个期刊
def get_periodicals(request,name):
    return HttpResponse('now name is %s' % (name))

# 访问具体文章
def get_paper(request,id):
    return HttpResponse('now id is %d' % (id))
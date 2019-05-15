from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
# Create your views here.
def login(request):
    pass

def register(request):
    pass

def profile(request,id):
    return HttpResponse('UserProfile id is %d' %(id))
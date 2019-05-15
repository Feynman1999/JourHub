from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse

def index(request):
    return HttpResponse('Hello World')

def about(request):
    return HttpResponse('About')
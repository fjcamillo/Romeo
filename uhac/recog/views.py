from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(requests):
    return HttpResponse('<h1>Hello Recog</h1>')

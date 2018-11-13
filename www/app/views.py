from django.shortcuts import render
from django.http import HttpResponse
from .domain.models import Account


# Create your views here.

def index(req):
    a = Account()
    return HttpResponse('Hello there')
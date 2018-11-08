from django.shortcuts import render
from django.http import HttpResponse
from www.app.domain import *


# Create your views here.
def index(req):
    a = Account()
    return HttpResponse('Hello there')
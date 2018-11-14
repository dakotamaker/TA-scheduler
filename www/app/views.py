from django.shortcuts import render
from django.http import HttpResponse
from .domain.CommandHandler import CommandHandler


# Create your views here.

ch = CommandHandler()

def index(req):
    cmd = req.GET.get('cmd', '')
    return HttpResponse(ch.ProcessCommand(cmd))
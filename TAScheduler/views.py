from django.shortcuts import render
from django.http import HttpResponse
from .domain.CommandHandler import CommandHandler
from django.views import View

# Create your views here.

ch = CommandHandler()

class index(View):

    def __init__(self, cmd):
        self.cmd = cmd
        self.return_str = ch.ProcessCommand(self.cmd)

    def get(self, request):
        return render(request, "main/index.html")
    def post(self, request):
        out = ch.ProcessCommand(self.cmd)
        return render(request, "main/index.html", {"out": out})

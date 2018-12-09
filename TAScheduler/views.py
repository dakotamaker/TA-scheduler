from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.template import loader
from .domain.CommandHandler import CommandHandler

# Create your views here.

ch = CommandHandler()


@require_http_methods(["GET"])
def index(request):
    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@require_http_methods(["POST"])
def command(request):
    r = ch.ProcessCommand(request.POST.get('cmd'))
    template = loader.get_template('main/index.html')
    context = {'out': r}
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def api(request):
    r = ch.ProcessCommand(request.GET.get('cmd'))
    return JsonResponse({'response': r})

class Home(View):

    def get(self, req):
        template = loader.get_template('main/index.html')
        context = {}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        pass

class Login(View):

    def get(self, req):
        pass

    def post(self, req):
        pass

class Logout(View):

    def get(self, req):
        pass

    def post(self, req):
        pass
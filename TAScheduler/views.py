from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.template import loader

from TAScheduler.forms.AssignLabForm import AssignLabForm
from TAScheduler.forms.CourseEmailForm import CourseEmailForm
from TAScheduler.forms.LabForm import LabForm
from TAScheduler.forms.UserEmailForm import UserEmailForm
from TAScheduler.forms.UserInfoForm import UserInfoForm
from TAScheduler.forms.NotifyForm import NotifyForm
from TAScheduler.forms.EditUserForm import EditUserForm
from TAScheduler.forms.EditForm import EditForm
from TAScheduler.forms.ViewCourseForm import ViewCourseForm
from TAScheduler.forms.ViewLabForm import ViewLabForm
from TAScheduler.forms.ViewUserForm import ViewUserForm
from .domain.CommandHandler import CommandHandler
from .domain.Role import Role
from TAScheduler.forms.CourseNameForm import CourseNameForm
from TAScheduler.forms.LoginForm import LoginForm
from TAScheduler.models import Account
from TAScheduler.domain.AvailableCommands import AvailableCommands

# Create your views here.

ch = CommandHandler()
avcmd = AvailableCommands()

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
        context = {'page_title': 'Home'}

        if 'current_role' in req.session:
            context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        else:
            context['cmds'] = []

        return HttpResponse(template.render(context, req))

class Login(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Login', 'form': LoginForm()}

        if 'current_role' in req.session:
            context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        else:
            context['cmds'] = []

        return HttpResponse(template.render(context, req))

    # this function is so gross because of the extra cases for logging in vs normal commands
    def post(self, req):
        form = LoginForm(req.POST)
        if form.is_valid():
            ch = CommandHandler()
            out = ch.ProcessCommand(f'login {form.cleaned_data["email"]} "{form.cleaned_data["password"]}"')
            if out.startswith('Logged in as'):
                template = loader.get_template('main/index.html')
                context = {'page_title': 'Home', 'out': out}
                req.session['current_user'] = form.cleaned_data['email']
                a = Account.objects.filter(act_email=form.cleaned_data['email']).first()
                req.session['current_role'] = a.role_id
            else:
                template = loader.get_template('main/form.html')
                context = {'page_title': 'Login', 'out': out, 'form': form}

            if 'current_role' in req.session:
                context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
            else:
                context['cmds'] = []

            return HttpResponse(template.render(context, req))
        else:
            template = loader.get_template('main/form.html')
            context = {'page_title': 'Login', 'form': form}

            if 'current_role' in req.session:
                context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
            else:
                context['cmds'] = []

            return HttpResponse(template.render(context, req))

class Logout(View):

    def post(self, req):
        template = loader.get_template('main/index.html')
        if req.session['current_user']:
            out = 'Successfully logged out'
        else:
            out = 'You must be logged in to log out'
        context = {'page_title': 'Home', 'out': out}
        req.session['current_user'] = None
        req.session['current_role'] = None
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

class CreateCourse(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Create Course', 'form': CourseNameForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CourseNameForm(req.POST)
        context = {'page_title': 'Create Course'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'create course "{form.cleaned_data["course_name"]}"')
            context['form'] = CourseNameForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class DeleteCourse(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Delete Course', 'form': CourseNameForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CourseNameForm(req.POST)
        context = {'page_title': 'Delete Course'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'delete course "{form.cleaned_data["course_name"]}"')
            context['form'] = CourseNameForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class CreateUser(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Create User', 'form': UserInfoForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = UserInfoForm(req.POST)
        context = {'page_title': 'Create User'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'create user {form.cleaned_data["email"]} "{form.cleaned_data["fname"]}" "{form.cleaned_data["lname"]}" {form.cleaned_data["role_id"]} {form.cleaned_data["phone"]} "{form.cleaned_data["address"]}" "{form.cleaned_data["office_hours"]}" "{form.cleaned_data["office_location"]}"')
            context['form'] = UserInfoForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class DeleteUser(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Delete User', 'form': UserEmailForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = UserEmailForm(req.POST)
        context = {'page_title': 'Delete User'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'delete user {form.cleaned_data["email"]}')
            context['form'] = UserEmailForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class CreateLab(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Create Lab', 'form': LabForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = LabForm(req.POST)
        context = {'page_title': 'Create Lab'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'create lab "{form.cleaned_data["course_name"]}" "{form.cleaned_data["lab_name"]}"')
            context['form'] = LabForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class DeleteLab(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Delete Lab', 'form': LabForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = LabForm(req.POST)
        context = {'page_title': 'Delete Lab'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'delete lab "{form.cleaned_data["course_name"]}" "{form.cleaned_data["lab_name"]}"')
            context['form'] = LabForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class AssignCourseTA(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Assign Course TA', 'form': CourseEmailForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CourseEmailForm(req.POST)
        context = {'page_title': 'Assign Course TA'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'assign course ta "{form.cleaned_data["course_name"]}" "{form.cleaned_data["email"]}"')
            context['form'] = CourseEmailForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class AssignCourseInstructor(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Assign Course Instructor', 'form': CourseEmailForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CourseEmailForm(req.POST)
        context = {'page_title': 'Assign Course Instructor'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'assign course instructor "{form.cleaned_data["course_name"]}" "{form.cleaned_data["email"]}"')
            context['form'] = CourseEmailForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class AssignLab(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Assign Lab', 'form': AssignLabForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = AssignLabForm(req.POST)
        context = {'page_title': 'Assign Lab'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(f'assign lab "{form.cleaned_data["course_name"]}" "{form.cleaned_data["lab_name"]}" "{form.cleaned_data["email"]}"')
            context['form'] = AssignLabForm()
        else:
            context['form'] = form
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class Notify(View):

    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Notify', 'form': NotifyForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = NotifyForm(req.POST)
        context = {'page_title': 'Notify'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(
                f'notify "{form.cleaned_data["email"]}" "{form.cleaned_data["subject"]}" "{form.cleaned_data["body"]}"')
            context['form'] = NotifyForm()
        else:
            context['form'] = form

        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class Edit(View):
    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Edit Information', 'form': EditForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        ##update only fields that have entries
        pass

class EditUser(View):
    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'Edit User Information', 'form': EditUserForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        ##update only fields that have entries
        pass

class ListTAs(View):
    def get(self, req):
        template = loader.get_template('main/index.html')
        context = {'page_title': 'List TAs', 'form': ""}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        ch = CommandHandler(req.session['current_user'])
        context['out'] = ch.ProcessCommand(
            f'list tas')
        return HttpResponse(template.render(context, req))

class ViewUser(View):
    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'View User', 'form': ViewUserForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = ViewUserForm(req.POST)
        context = {'page_title': 'View User'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(
                f'view user "{form.cleaned_data["email"]}"')
            context['form'] = ViewUserForm()
        else:
            context['form'] = form

        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class ViewCourse(View):
    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'View Course', 'form': ViewCourseForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = ViewCourseForm(req.POST)
        context = {'page_title': 'View Course'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(
                f'view course "{form.cleaned_data["course"]}"')
            context['form'] = ViewCourseForm()
        else:
            context['form'] = form

        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))

class ViewLab(View):
    def get(self, req):
        template = loader.get_template('main/form.html')
        context = {'page_title': 'View Lab', 'form': ViewLabForm()}
        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = ViewLabForm(req.POST)
        context = {'page_title': 'View Lab'}
        if form.is_valid():
            ch = CommandHandler(req.session['current_user'])
            context['out'] = ch.ProcessCommand(
                f'view lab "{form.cleaned_data["course"]}" "{form.cleaned_data["lab"]}"')
            context['form'] = ViewLabForm()
        else:
            context['form'] = form

        context['cmds'] = avcmd.getAvailableCommands(req.session['current_role'])
        template = loader.get_template('main/form.html')
        return HttpResponse(template.render(context, req))


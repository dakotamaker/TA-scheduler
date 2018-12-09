"""ta_scheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
import TAScheduler.views as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', views.Home.as_view()),
    path('login', views.Login.as_view()),
    path('logout', views.Logout.as_view()),
    path('create-course', views.CreateCourse.as_view()),
    path('delete-course', views.DeleteCourse.as_view()),
    path('create-user', views.CreateUser.as_view())
]

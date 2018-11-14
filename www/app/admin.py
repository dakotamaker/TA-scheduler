from django.contrib import admin
from .domain.models.Account import Account
from .domain.models.Course import Course
from .domain.models.Lab import Lab


# Register your domain here.
admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Lab)
from django.db import models
from . import Course
from . import Account

class Lab(models.Model):

    lab_id = models.IntegerField(primary_key=True)
    lab_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)

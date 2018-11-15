from django.db import models
from . import Account


class Course(models.Model):

    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=50, unique=True)
    instructor = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    tas = models.ManyToManyField(Account, blank=True, related_name='courses')
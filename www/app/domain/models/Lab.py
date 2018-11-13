from django.db import models
from . import Course
from . import Account

class Lab(models.Model):

    lab_id = models.IntegerField(primary_key=True)
    lab_name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta_email = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return (str(self.lab_id) + ' | ' +
                self.lab_name + ' | ' +
                str(self.course_id) + ' | ' +
                self.ta_email)

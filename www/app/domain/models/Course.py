from django.db import models
from . import Account


class Course(models.Model):

    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=50)
    instructor_email = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL, related_name='instructor_email')
    ta_emails = models.ManyToManyField(Account, related_name='ta_email')

    def __str__(self) -> str:
        return (str(self.course_id) + ' | ' +
                self.course_name + ' | ' +
                self.instructor_email)

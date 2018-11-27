from django.db import models
from .domain.Role import Role


# Create your models here.
class Account(models.Model):

    act_email = models.EmailField(primary_key=True)
    act_fname = models.CharField(max_length=50)
    act_lname = models.CharField(max_length=50)
    act_phone = models.CharField(max_length=15)
    act_password = models.CharField(max_length=50)
    act_address = models.CharField(max_length=255)
    act_officehours = models.CharField(max_length=15)
    act_officelocation = models.CharField(max_length=255)
    role_id = models.SmallIntegerField()

    def RoleIn(self, *roles: [Role]) -> bool:
        return Role(self.role_id) in roles

class Course(models.Model):

    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50, unique=True)
    instructor = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    tas = models.ManyToManyField(Account, blank=True, related_name='courses')


class Lab(models.Model):

    lab_id = models.AutoField(primary_key=True)
    lab_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)

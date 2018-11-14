from django.db import models
from ..Role import Role


class Account(models.Model):

    act_email = models.EmailField(primary_key=True)
    act_fname = models.CharField(max_length=50)
    act_lname = models.CharField(max_length=50)
    act_phone = models.CharField(max_length=15)
    act_password = models.CharField(max_length=50)
    act_address = models.CharField(max_length=255)
    role_id = models.SmallIntegerField()

    def RoleIn(self, *roles: [Role]) -> bool:
        return Role(self.role_id) in roles

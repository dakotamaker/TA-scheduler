from django.db import models
from .. import Role


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

    def __str__(self) -> str:
        return (self.act_email + ' | ' +
                self.act_fname + ' | ' +
                self.act_lname + ' | ' +
                self.act_password + ' | ' +
                self.act_phone + ' | ' +
                self.act_address + ' | ' +
                str(Role(self.role_id)).split('.', 1)[1])

from django.db import models
from datetime import date


# Create your models here.
class AccountRequest(models.Model):
    username = models.CharField(max_length=127)
    email = models.EmailField(max_length=127)
    institute_name = models.CharField(max_length=127)
    institute_iso = models.CharField(max_length=127)

    approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(default=date.today)
    approval_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.username + ' - ' + self.institute_name)


class Account(models.Model):
    account = models.OneToOneField(AccountRequest, on_delete=models.CASCADE)
    password = models.CharField(max_length=127)

    # Account Database Details
    db_engine = models.CharField(max_length=127)
    db_name = models.CharField(max_length=127)
    db_user = models.CharField(max_length=127)
    db_password = models.CharField(max_length=127)
    db_host = models.CharField(max_length=127)
    db_port = models.CharField(max_length=127)

    def __str__(self):
        username = str(self.account)
        return username

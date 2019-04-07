from django.db import models
from django.utils import timezone


# Create your models here.
class AccountRequest(models.Model):
    username = models.CharField(max_length=127)
    email = models.EmailField(max_length=127)
    institute_name = models.CharField(max_length=127)
    institute_iso = models.CharField(max_length=127)

    approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(default=timezone.now)
    approval_date = models.DateTimeField(null=True)

    status = models.CharField(max_length=63, default='Inactive')
    account_link = models.OneToOneField('Account', related_name='account_link', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username + ' - ' + self.institute_name)


class Account(models.Model):
    user_account = models.OneToOneField(AccountRequest, on_delete=models.CASCADE)
    user_password = models.CharField(max_length=127)

    # Account Database Details
    db_engine = models.CharField(max_length=127)
    db_name = models.CharField(max_length=127)
    db_user = models.CharField(max_length=127)
    db_password = models.CharField(max_length=127)
    db_host = models.CharField(max_length=127)
    db_port = models.CharField(max_length=127)

    def __str__(self):
        return str(self.user_account.username)

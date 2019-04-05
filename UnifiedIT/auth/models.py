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

    def __str__(self):
        return str(self.username + ' - ' + self.institute_name)
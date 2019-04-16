from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)

# Create your models here.

CHAR_FIELD_MAX_LENGTH = 63


class User(AbstractUser):
    account_link = models.OneToOneField('Account', related_name='user_account_link', on_delete=models.CASCADE, null=True,
                                        default=None)

    is_institute_admin = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    def create_user(self, username, email, is_institute_admin, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_institute_admin=is_institute_admin,
        )
        user.is_staff = True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_institute_admin = False
        user.save()

        return user


class AccountRequest(models.Model):
    username = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    email = models.EmailField(max_length=CHAR_FIELD_MAX_LENGTH)
    institute_name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    institute_iso = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

    approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(default=timezone.now)
    approval_date = models.DateTimeField(null=True)

    account_link = models.OneToOneField('Account', related_name='account_link', on_delete=models.SET_NULL, null=True,
                                        default=None)

    def __str__(self):
        return str(self.username)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.OneToOneField(AccountRequest, on_delete=models.SET_NULL, null=True)
    db_key = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (SUSPENDED, 'Suspended')
    )

    status = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH,
                              choices=STATUS_CHOICES, default=ACTIVE)

    # Account Database Details
    db_engine = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    db_name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    db_user = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    db_password = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    db_host = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    db_port = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

    def __str__(self):
        return str(self.details.username)

import json

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)

# Create your models here.

CHAR_FIELD_MAX_LENGTH = 63


class User(AbstractUser):
    account_link = models.OneToOneField('Account', related_name='user_account_link', on_delete=models.CASCADE,
                                        null=True, default=None, blank=True)

    is_institute_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)  # TODO: Authentication on basis of 'is_institute_admin'.

    def has_perm(self, perm, obj=None):
        app_label = perm.split('.')[0]
        if self.is_institute_admin:
            return app_label == 'Profiler'
        if self.is_superuser:
            return app_label == 'Accountant'

    def has_module_perms(self, app_label):
        if self.is_institute_admin:
            return app_label == 'Profiler'
        if self.is_superuser:
            return app_label == 'Accountant'


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

    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'
    DEAD = 'dead'

    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (DEAD, 'Dead')
    )

    status = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH,
                              choices=STATUS_CHOICES, default=PENDING)

    request_date = models.DateTimeField(default=timezone.now)
    approval_date = models.DateTimeField(null=True)

    account_link = models.OneToOneField('Account', related_name='account_link', on_delete=models.SET_NULL, null=True,
                                        default=None)

    def __str__(self):
        return str(self.username)


class JSONField(models.CharField):
    """
    JSON data gets stored as string in database.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1023
        super(JSONField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.OneToOneField(AccountRequest, on_delete=models.SET_NULL, null=True)
    db_key = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    db_details = JSONField()

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

    def __str__(self):
        return str(self.details.username)

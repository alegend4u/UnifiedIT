from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional
    dob = models.DateField()

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    start_date = models.DateField()

    address_link = models.OneToOneField('Address', related_name='address', on_delete=models.CASCADE)
    contacts_link = models.ForeignKey('Contact', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    street = models.CharField(max_length=31)
    city = models.CharField(max_length=31)
    state = models.CharField(max_length=31)
    pincode = models.CharField(max_length=15)

    def __str__(self):
        return self.city + ', ' + self.state


class Contact(models.Model):
    value = models.CharField(max_length=12)

    def __str__(self):
        return self.value


from django.db import models

# Create your models here.
MAX_LENGTH = 31


class Person(models.Model):
    username = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField(max_length=MAX_LENGTH)
    password = models.CharField(max_length=MAX_LENGTH)
    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)

    # Additional
    dob = models.DateField()

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)

    start_date = models.DateField()
    address_link = models.OneToOneField('Address', related_name='address', on_delete=models.CASCADE, null=True, blank=True)
    contacts_link = models.ForeignKey('Contact', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    street = models.CharField(max_length=MAX_LENGTH)
    city = models.CharField(max_length=MAX_LENGTH)
    state = models.CharField(max_length=MAX_LENGTH)
    pincode = models.CharField(max_length=15)

    def __str__(self):
        return self.city + ', ' + self.state


class Contact(models.Model):
    value = models.CharField(max_length=12)

    def __str__(self):
        return self.value


class Faculty(models.Model):
    designation = models.CharField(max_length=MAX_LENGTH)
    qualification = models.CharField(max_length=MAX_LENGTH)


class Student(models.Model):
    sid = models.CharField(max_length=MAX_LENGTH)
    roll_no = models.IntegerField()
    semester = models.IntegerField()
    admission_type = models.CharField(max_length=MAX_LENGTH)
    is_d2d = models.BooleanField(default=False)
    degree = models.CharField(max_length=MAX_LENGTH)
    caste_category = models.CharField(max_length=MAX_LENGTH)
    nationality = models.CharField(max_length=MAX_LENGTH)
    blood_group = models.CharField(max_length=MAX_LENGTH)
    guardian_name = models.CharField(max_length=MAX_LENGTH)
    guardian_relation = models.CharField(max_length=MAX_LENGTH)

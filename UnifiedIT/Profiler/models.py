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
    address_link = models.ForeignKey('Address', related_name='address', on_delete=models.CASCADE, null=True, blank=True)
    Dep_link = models.ForeignKey('Department',related_name='department',on_delete=models.CASCADE,null= True, blank = True)
    def __str__(self):
        return self.username


class Address(models.Model):
    #person = models.OneToOneField(Person, on_delete=models.CASCADE)
    street = models.CharField(max_length=MAX_LENGTH)
    city = models.CharField(max_length=MAX_LENGTH)
    state = models.CharField(max_length=MAX_LENGTH)
    pincode = models.CharField(max_length=15)

    def __str__(self):
        return self.city + ', ' + self.state


class Contact(models.Model):
    value = models.CharField(max_length=12)
    Person_link = models.ForeignKey('Person', related_name='contacts',on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.Person_link


class Department(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    dept_code = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.name


class Faculty(Person):
    designation = models.CharField(max_length=MAX_LENGTH)
    qualification = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.designation



class Student(Person):
    roll_no = models.IntegerField()
    semester = models.IntegerField()
    admission_type = models.CharField(max_length=MAX_LENGTH)
    is_d2d = models.BooleanField(default=False)
    degree = models.CharField(max_length=MAX_LENGTH)
    cast_category = models.CharField(max_length=MAX_LENGTH)
    nationality = models.CharField(max_length=MAX_LENGTH)

    Aneg = 'A-'
    Apos = 'A+'
    Bneg = 'B-'
    Bpos = 'B+'
    ABneg = 'AB-'
    ABpos='AB+'
    Opos='O+'
    Oneg='O-'
    BLOODGROUP_CHOICES = ((Aneg, 'A-'), (Apos, 'A+'),(Bneg,'B-'),(Bpos,'B+'),(ABneg,'AB-'),(ABpos,'AB+'),(Opos,'O+'),(Oneg,'O-'))
    blood_group = models.CharField(max_length=MAX_LENGTH,choices=BLOODGROUP_CHOICES,default=Apos)
    guardian_name = models.CharField(max_length=MAX_LENGTH)
    guardian_relation = models.CharField(max_length=MAX_LENGTH)
    #Must have an field of passingYear like we have passing year of 2020....


class Course(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    duration = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)
    department = models.ForeignKey('Department',on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    is_theory = models.BooleanField(default=False)
    duration = models.CharField(max_length=MAX_LENGTH)


class SessPrac(models.Model):
    session = models.OneToOneField('Session',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.session.is_theory) + str(self.session.duration)

class SessTheory(models.Model):
    faculty = models.ForeignKey('Faculty',on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.username


class Subject(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    semester = models.CharField(max_length=MAX_LENGTH)
    credits = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)
    course = models.ForeignKey('Course',on_delete=models.CASCADE, null=True, blank=True)
    session = models.ManyToManyField(Session)

    def __str__(self):
        return self.name
    
class Division(models.Model):
    label = models.CharField(max_length=MAX_LENGTH)
    semester = models.CharField(max_length=MAX_LENGTH)
    course= models.ForeignKey('Course',on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.label+','+self.semester

class Batch(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    division = models.ForeignKey('Division',on_delete=models.CASCADE, null=True, blank=True)
    sess_prac = models.ForeignKey('Sessprac',on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    THEORY = 'Theory'
    PRACTICAL = 'Practical'
    EXAM_CHOICES = ((THEORY, 'Theory'), (PRACTICAL, 'Practical'))
    theory_prac = models.CharField(max_length=MAX_LENGTH,choices=EXAM_CHOICES,default=THEORY)
    isRemedial = models.BooleanField(default=False)
    course = models.ForeignKey('Course',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)#aa na samajaanu
    exam = models.ForeignKey('Exam',on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE)
    score = models.IntegerField()
    max_marks = models.IntegerField()
    duration = models.CharField(max_length=MAX_LENGTH)
    date_of_exam = models.DateField()

    def __str__(self):
        return str(self.student.roll_no)

class ToBeCovered(models.Model):
    date = models.DateField()

class TimeTable(models.Model):
    division = models.ForeignKey('Division',on_delete=models.CASCADE)
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY='Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    DAY_CHOICES = ((MONDAY, 'Mon'), (TUESDAY, 'Tue'),(WEDNESDAY,'Wed'),(THURSDAY,'Thu'),(FRIDAY,'Fri'),(SATURDAY,'Sat'))
    day = models.CharField(max_length=MAX_LENGTH,choices=DAY_CHOICES)
    seq_no = models.IntegerField()
    session=models.ForeignKey('Session',on_delete=models.CASCADE)
    start_time = models.DateField()
    location = models.CharField(max_length=MAX_LENGTH)
    to_be_covered = models.ManyToManyField(ToBeCovered)

    def __str__(self):
        return self.division.label+','+self.division.semester


class Attendance(models.Model):
    timetable=models.ForeignKey('TimeTable',on_delete=models.CASCADE)
    student= models.ForeignKey('Student',on_delete=models.CASCADE)
    PRESENT= 1
    ABSENT = 0
    STATUS_CHOICES= ((0,'Absent'),(1,'Present'))
    status = models.IntegerField(choices=STATUS_CHOICES,default=0)
    date = models.DateField()

    def __str__(self):
        return str(self.student.roll_no)+','+str(self.timetable.day)

class Topic(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)
    to_be_covered= models.ManyToManyField(ToBeCovered)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE)

    def __str__(self):
        return self.name + self.subject

class FacultyIncharge(models.Model):
    faculty= models.ManyToManyField(Faculty)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return self.faculty.username+','+self.subject.name
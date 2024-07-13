from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Medications(models.Model):
    patientid = models.IntegerField()
    doctorid = models.IntegerField()
    doctorname = models.CharField(max_length=80)
    medicinename = models.CharField(max_length=80)
    quantity = models.CharField(max_length=80)
    days = models.CharField(max_length=80)
    time = models.CharField(max_length=80)

    def __str__(self):
        return self.medicinename

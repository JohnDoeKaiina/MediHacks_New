from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class HealthInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    blood_type = models.CharField(max_length=10)
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)

    def __str__(self):
        return f"Health info for {self.user.username}"

class EmergencyContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Emergency contact for {self.user.username}"


class Prescrition(models.Model):
    patientid = models.IntegerField()
    medicinename = models.CharField(max_length=80)
    quantity = models.CharField(max_length=80)
    days = models.CharField(max_length=80)
    time = models.CharField(max_length=80)

    def __str__(self):
        return self.medicinename

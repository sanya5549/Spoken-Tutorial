from django.db import models
from django.contrib.auth.models import User


class Foss(models.Model):
    fossname = models.CharField(max_length=20, primary_key=True)
    class Meta:
        ordering = ('fossname',)
    def __str__(self):
        return self.fossname


class Userdetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, max_length=15, primary_key=True)
    email = models.EmailField(User, max_length=30)
    password = models.CharField(User, max_length=20)
    fossname = models.OneToOneField(Foss, on_delete=models.CASCADE, null=True)


class Tutorialdetails(models.Model):
    tname = models.CharField(max_length=50)
    fossname = models.ForeignKey(Foss, on_delete=models.CASCADE)
    submdate = models.DateField('date published', null=True)
    deadline = models.DateField('date')

    class Meta:
        unique_together=(("tname","fossname"),)


class Payment(models.Model):
    user = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default=0)
    def __int__(self):
        return self.user_id


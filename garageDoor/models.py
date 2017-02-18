from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class door(models.Model):
    doorName = models.CharField(max_length = 200)
    doorID = models.AutoField(primary_key = True)
    currentState = models.CharField(max_length = 50, default='closed')
    lastChanged = models.DateTimeField()
    sensorPin = models.IntegerField()
    relayPin = models.IntegerField()
    def __str__(self):
        return self.doorName

class openEvent(models.Model):
    #user = models.ForeignKey()
    openID = models.AutoField(primary_key = True)
    openTime = models.DateTimeField()
    door = models.ForeignKey('door',on_delete = models.CASCADE, related_name ='doorOpened')

    def __str__(self):
        return " " + str(self.door) + " " +str(self.openTime)


class closeEvent(models.Model):
    #user= models.ForeignKey()
    closeTime = models.DateTimeField()
    closeID = models.AutoField(primary_key = True)
    door = models.ForeignKey('door',on_delete = models.CASCADE, related_name ='doorClosed')

    def __str__(self):
        return " " + str(self.door) + " " +str(self.closeTime)

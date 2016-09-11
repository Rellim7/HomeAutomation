from __future__ import unicode_literals

from django.db import models

# Create your models here.
class door(models.Model):
    doorName = models.CharField(maxlength = 200)
    doorID = models.AutoField(primary_key = True)
    currentState = models.CharFeild(max_length = 50)
    lastChanged = models.DateTimeField()
    sensorPin = models.IntegerField()
    relayPin = models.IntegerField()
    def __str__(self):
        return self.doorName

class openEvent(models.Model):
    user = models.ForeignKey()
    openID = models.AutoField(primary_key = True)
    openTime = models.DateTimeField()
    door = models.ForeignKey()

    def __str__(self):
        return self.user + " " + str(self.door) + " " +self.openTime


class closeEvent(models.Model):
    user= models.ForeignKey()
    closeTime = models.DateTimeField()
    closeID = models.AutoField(primary_key = True)
    door = models.ForeignKey()

    def __str__(self):
        return self.user + " " + str(self.door) + " " +self.openTime

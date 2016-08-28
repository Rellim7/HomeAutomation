from __future__ import unicode_literals

from django.db import models

# Create your models here.
class door(models.Model):
    doorName = models.CharFeild(maxlength = 200)
    doorID = models.AutoField(primary_key = True)
    currentState = models.CharFeild(max_length = 50)
    lastChanged = models.DateTimeField()


class openEvent(models.Model):
    user = models.ForeignKey()
    openID = models.AutoFeild(primary_key = True)
    openTime =
    door = models.ForeignKey()

class closeEvent(models.Model):
    user= models.ForeignKey()
    closeTime = models.DateTimeField()
    closeID = models.AutoField(primary_key = True)
    door = models.ForeignKey()

from django.db import models

class DefaultConfig(models.Model):
    decimalesCant = models.IntegerField(default=2)
    decimalesChar = models.CharField(default='.', max_length=1)
    milesChar = models.CharField(default=',', max_length=1)

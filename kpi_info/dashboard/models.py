from django.db import models

class Revenue(models.Model):
    money = models.IntegerField()
    datetime = models.DateTimeField()

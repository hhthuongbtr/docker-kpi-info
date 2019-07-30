from django.db import models

class Revenue(models.Model):
    id = models.CharField(max_length=100, primary_key=True, verbose_name='ID')
    money = models.IntegerField()
    datetime = models.DateTimeField()

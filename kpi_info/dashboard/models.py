from django.db import models
from django.db.models import Sum
import datetime

class Revenue(models.Model):
    id = models.CharField(max_length=100, primary_key=True, verbose_name='ID')
    money = models.IntegerField()
    datetime = models.DateTimeField()

    # Get total revenue in specific time range
    def get_from_range(self, start_time, end_time):
        transaction_in_range = Revenue.objects.filter(
            datetime__range = (start_time, end_time),
        ).annotate(
            hourly_revenue = Sum('money')
        )
        return sum(transaction.money for transaction in transaction_in_range)
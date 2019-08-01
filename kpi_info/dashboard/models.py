from django.db import models
from django.db.models import Sum
from datetime import datetime, timedelta

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

    # Get total revenue in specific hour of specific day
    def get_hourly(self, date, time):
        values = self.model.objects.filter(
            datetime__range=(date, time)
        ).values('datetime').annotate(data_sum=Sum('data'))
        return "12345"

    # Get total revenue from 00:00 to a specific hour of the day
    def get_day_total_at_hour(self, date, time):
        return "54321"
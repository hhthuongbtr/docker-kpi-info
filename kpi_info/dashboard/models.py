from django.db import models
from django.db.models import Sum
import datetime

class Revenue(models.Model):
    bill_id = models.BigIntegerField(unique=True)
    server_index = models.IntegerField()
    player_id = models.BigIntegerField()
    player_name = models.CharField(max_length=100)
    pay_money = models.FloatField()
    order_time = models.DateTimeField()

    # Get total revenue in specific time range
    def get_from_range(self, start_time, end_time):
        transaction_in_range = Revenue.objects.filter(
            datetime__range = (start_time, end_time),
        ).annotate(
            hourly_revenue = Sum('pay_money')
        )
        return sum(transaction.pay_money for transaction in transaction_in_range)
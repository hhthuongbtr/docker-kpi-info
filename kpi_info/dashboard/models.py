from django.db import models
from django.db.models import Sum, Count
import datetime

class Revenue(models.Model):
    bill_id = models.BigIntegerField(unique=True)
    server_index = models.IntegerField()
    player_id = models.BigIntegerField()
    player_name = models.CharField(max_length=100)
    pay_money = models.IntegerField()
    order_time = models.DateTimeField()

    # Get total revenue in specific time range
    def get_from_range(self, start_time, end_time):
        transaction_in_range = Revenue.objects.filter(
            order_time__range = (start_time, end_time),
        ).annotate(
            hourly_revenue = Sum('pay_money')
        )
        return sum(transaction.pay_money for transaction in transaction_in_range)

    @staticmethod
    def get_top_paid_users(start_date=None, end_date=None, server_index=None, count=None):
        transactions = Revenue.objects.all()
        # Filter by date time range
        if start_date and end_date:
            transactions = transactions.filter(
                order_time__range = (datetime.datetime.combine(start_date, datetime.time.min),
                                     datetime.datetime.combine(end_date, datetime.time.max))
            )
        # Filter by server index
        if server_index:
            transactions = transactions.filter(
                server_index = server_index
            )
        # Get ordered list of top paid users
        top_users = transactions.values(
            'player_name',
            'server_index',
        ).annotate(
            total_pay_money=Sum('pay_money')
        ).order_by('-total_pay_money')
        # Limit top users list length if needed
        if count:
            top_users = top_users[:count]
        return top_users

    @staticmethod
    def get_item_sales(start_date=None, end_date=None, server_index=None):
        transactions = Revenue.objects.all()
        if start_date and end_date:
            transactions = transactions.filter(
                order_time__range = (datetime.datetime.combine(start_date, datetime.time.min),
                                     datetime.datetime.combine(end_date, datetime.time.max))
            )
        if server_index:
            transactions = transactions.filter(
                server_index = server_index
            )
        unit_sales = transactions.values("pay_money").annotate(Count("id"))
        return unit_sales
    
    @staticmethod
    def get_server_list():
        return Revenue.objects.values_list("server_index", flat=True).distinct().order_by("server_index")

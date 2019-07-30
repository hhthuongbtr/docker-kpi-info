from django.core.management.base import BaseCommand, CommandError
from ...models import Revenue
from django.db.models import Sum
import csv
import datetime


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        logfile = open('data/nikki/20190701/2019-06-02/nikkisea_datalog_chargelog_hourly/Nikki_Logcharge_2019-06-01-00.csv', encoding="latin-1")
        log = csv.DictReader(logfile)

        revenue = Revenue()

        for row in log:
            revenue.money = row["money"]
            revenue.datetime = datetime.datetime.strptime("2019-05-31 23:24:29", '%Y-%m-%d %H:%M:%S')
            revenue.save()
            print(Revenue.objects.aggregate(Sum('money')))

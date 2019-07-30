from django.core.management.base import BaseCommand, CommandError
from ...models import Revenue
from django.db.models import Sum
import csv
import datetime


class Command(BaseCommand):
    help = 'Parse data from CSV log file'

    def handle(self, *args, **options):
        logfile = open('data/nikki/20190701/2019-06-02/nikkisea_datalog_chargelog_hourly/Nikki_Logcharge_2019-06-01-00.csv', encoding="latin-1")
        log = csv.DictReader(logfile)

        revenue = Revenue()

        for row in log:
            revenue.id = row["transid"]
            revenue.money = row["money"]
            datetime_from_transid = revenue.id[:revenue.id.find("-")]
            revenue.datetime = datetime.datetime.strptime(datetime_from_transid, '%Y%m%d%H%M%S')
            revenue.save()
            print(revenue.id)
            print(revenue.money)
            print(revenue.datetime)
            print(Revenue.objects.aggregate(Sum('money')))

from django.core.management.base import BaseCommand, CommandError
from ...models import Revenue
from django.db.models import Sum
import csv
import datetime
import glob

class Command(BaseCommand):
    help = 'Parse data from CSV log file'

    def handle(self, *args, **options):
        log_dir = 'data/nikki/*/*/nikkisea_datalog_chargelog_hourly/*.csv'
        for log in glob.iglob(log_dir):
            self.write_log_to_db(log)

    def readlog(self, log_path):
        logfile = open(log_path, encoding='latin-1')
        return csv.DictReader(logfile)

    def write_log_to_db(self, log_path):
        log = self.readlog(log_path)
        revenue = Revenue()

        for row in log:
            revenue.id = row["transid"]
            revenue.money = row["money"]
            datetime_from_transid = revenue.id[:revenue.id.find("-")]
            revenue.datetime = datetime.datetime.strptime(datetime_from_transid, '%Y%m%d%H%M%S')
            revenue.save()
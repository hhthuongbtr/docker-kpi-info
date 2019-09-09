from django.core.management.base import BaseCommand, CommandError
from ...models import Revenue
from django.db.models import Sum
import csv
import datetime
import time
import glob
import os

class Command(BaseCommand):
    help = 'Parse data from CSV log file'

    def handle(self, *args, **options):
        log_dir = 'data/nikki/*/*/nikkisea_datalog_chargelog_hourly/*.csv'
        for log in glob.iglob(log_dir):
            if os.path.exists('last_updated'):
                with open('last_updated', 'r') as f:
                    last_updated = float(f.read())
                if last_updated > os.path.getmtime(log):
                    continue

            self.write_log_to_db(log)

        with open('last_updated', 'w') as f:
            f.write(str(time.time()))

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
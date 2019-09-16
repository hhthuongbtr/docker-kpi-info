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
        # data
        # ├── loggame_20190904 <- log by date
        # │   ├── 25001 <- log by server
        # │   │   ├── recharge.csv
        # │   │   ├── shop.csv
        # ...
        data_dir = 'data'
        log_by_date_list = next(os.walk('{}/'.format(data_dir)))[1]
        for log_by_date in log_by_date_list:
            if os.path.exists('last_updated'):
                with open('last_updated', 'r') as f:
                    last_updated = float(f.read())
                if last_updated > os.path.getmtime('{}/{}/'.format(data_dir, log_by_date)):
                    continue

            server_id_list = self.get_server_id_list('{}/{}/serverlist.csv'.format(data_dir, log_by_date))
            for server_id in server_id_list:
                self.write_log_to_db(self.get_log_path(data_dir, log_by_date, server_id, 'recharge'), server_id)

        with open('last_updated', 'w') as f:
            f.write(str(time.time()))

    def get_log_path(self, data_dir, date_dir, server_id, log_type):
        return "{}/{}/{}/{}.csv".format(data_dir, date_dir, server_id, log_type)

    def get_server_id_list(self, serverlist_path):
        serverlist = self.read_log(serverlist_path)
        server_id_list = []
        for row in serverlist:
            server_id_list.append(row["ServerID"])
        return server_id_list

    def read_log(self, log_path):
        logfile = open(log_path)
        return csv.DictReader(logfile, delimiter='\t', quoting=csv.QUOTE_NONE)

    def readlog(self, log_path):
        logfile = open(log_path, encoding='latin-1')
        return csv.DictReader(logfile)

    def write_log_to_db(self, log_path, server_index):
        log = self.read_log(log_path)

        for row in log:
            Revenue.objects.update_or_create(
                bill_id = row["BillID"],
                server_index = server_index,
                player_id = row["PlayerID"],
                player_name  = row["PlayerName"].encode('utf-8'),
                pay_money = row["pay_money"],
                order_time = datetime.datetime.strptime(row["order_time"], '%Y-%m-%d %H:%M:%S'),
            )
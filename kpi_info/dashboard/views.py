from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .models import Revenue
from datetime import datetime, timedelta

def dashboard(request):
    return render(request, 'dashboard/index.html')

COLORS = [
    (210, 214, 222),  # Light gray
    (60, 141, 188),   # Blue
]

def next_color(color_list=COLORS):
    step = 0
    while True:
        for color in color_list:
            yield list(map(lambda base: (base + step) % 256, color))
        step += 197

class ChartJSONView(BaseLineChartView):
    def get_labels(self):
        return list(range(0, 24))

    def get_providers(self):
        return ["31/06/2019 hourly", "31/06/2019 total", "01/07/2019 hourly", "01/07/2019 total"]

    def get_datasets(self):
        datasets = []
        color_generator = self.get_colors()
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, entry in enumerate(data):
            color = tuple(next(color_generator))
            dataset = {'borderColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointBackgroundColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointBorderColor': "#fff",
                       'data': entry}
            dataset['backgroundColor'] = dataset['borderColor']
            dataset['pointBackgroundColor'] = dataset['pointBorderColor']
            if i < num:
                dataset['label'] = providers[i]  # series labels for Chart.js
            if i % 2 == 1:
                dataset['type'] = "line"
                dataset['fill'] = False
            datasets.append(dataset)
        return datasets

    def get_data(self):
        day1 = datetime.strptime('2019-06-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        day2 = datetime.strptime('2019-05-31 00:00:00', '%Y-%m-%d %H:%M:%S')
        return [self.get_day_hourly_data(day1),
                self.get_day_hourly_data(day2),]
                # [6280, 23119, 7189, 24027, 8097, 24936, 25844, 9915, 26753, 10823, 11732, 28570, 12641, 29479, 13549, 30387, 14458, 31296, 15366, 32205, 16275, 345, 17184, 1254, 19484],
                # [28938, 13008, 29846, 13917, 30755, 14825, 31663, 15734, 32572, 16642, 713, 17551, 1621, 18460, 2530, 19368, 3439, 20277, 4347, 21185, 5256, 22094, 6164, 23003, 26212],
                # [26405, 10476, 27314, 11384, 28223, 12293, 29131, 13202, 30040, 14110, 30948, 15019, 31857, 15927, 32766, 16836, 906, 17745, 1815, 18653, 2724, 19562, 3632, 20470, 22771],]

    def get_hourly_data(self, datetime):
        revenue = Revenue()
        return revenue.get_from_range(datetime, datetime + timedelta(hours=1))

    # Get list of hourly revenue from 0h to 24h of a specific day
    def get_day_hourly_data(self, datetime):
        day_hourly = []
        for i in range(24):
            hourly_revenue = self.get_hourly_data(datetime + timedelta(hours=i))
            print(hourly_revenue)
            day_hourly.append(hourly_revenue)
        return day_hourly

    def get_colors(self):
        return next_color()
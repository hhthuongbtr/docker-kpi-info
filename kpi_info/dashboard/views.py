from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .models import Revenue
from datetime import datetime, timedelta
from .forms import DateForm

def dashboard(request):
    form = DateForm()
    return render(request, 'dashboard/index.html', {'form': form})

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
        day1 = datetime.strptime('2019-06-01', '%Y-%m-%d')
        day2 = datetime.strptime('2019-05-31', '%Y-%m-%d')
        return [self.get_daily_data(day1, 'hourly'),
                self.get_daily_data(day1, 'total'),
                self.get_daily_data(day2, 'hourly'),
                self.get_daily_data(day2, 'total'),]

    def get_hourly_data(self, datetime):
        revenue = Revenue()
        return revenue.get_from_range(datetime, datetime + timedelta(hours=1))

    def get_total_at_hour_data(self, datetime):
        revenue = Revenue()
        return revenue.get_from_range(datetime.replace(hour=0, minute=0, second=0), datetime)

    def get_daily_data(self, date, type):
        daily_data = []
        date = date.replace(hour=0, minute=0, second=0) # Only date needed
        for i in range(24):
            if type == 'hourly':
                hour_data = self.get_hourly_data(date + timedelta(hours=i))
            elif type == 'total':
                hour_data = self.get_total_at_hour_data(date + timedelta(hours=i))
            else:
                print('Revenue data type invalid')
            daily_data.append(hour_data)
        return daily_data

    def get_colors(self):
        return next_color()
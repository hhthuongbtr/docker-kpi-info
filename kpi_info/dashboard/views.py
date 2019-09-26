from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .models import Revenue
from datetime import datetime, timedelta
from .forms import DateRangeForm, ServerDateRangeForm
from django.http import HttpResponseRedirect
from django.urls import resolve
import json
from django.db.models import Sum

def dashboard(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            return render(request, 'dashboard/compare.html', {'form': form, 'date1': start_date.strftime("%Y-%m-%d"), 'date2': end_date.strftime("%Y-%m-%d")})
    else:
        form = DateRangeForm()

    return render(request, 'dashboard/index.html', {'form': form})

COLORS = [
    "#23AEBB",
    "#f56954",
    "#00a65a",
    "#00c0ef",
    "#f39c12",
    "#0073b7",
    "#001F3F",
    "#39CCCC",
    "#3D9970",
    "#01FF70",
    "#FF851B",
    "#F012BE",
    "#8E24AA",
    "#D81B60",
    "#222222",
    "#d2d6de"
]

def next_color(color_list=COLORS):
    while True:
        for color in color_list:
            yield color

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
        date1 = datetime.strptime(self.kwargs['date1'], '%Y-%m-%d')
        date2 = datetime.strptime(self.kwargs['date2'], '%Y-%m-%d')
        return [self.get_daily_data(date1, 'hourly'),
                self.get_daily_data(date1, 'total'),
                self.get_daily_data(date2, 'hourly'),
                self.get_daily_data(date2, 'total'),]

    def get_hourly_data(self, datetime):
        revenue = Revenue()
        return revenue.get_from_range(datetime, datetime + timedelta(hours=1)) * 10

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

def top_users(request):
    top_users = Revenue.get_top_paid_users()
    server_list = Revenue.get_server_list()
    return render(request, 'dashboard/top_users.html', {'top_users': top_users, 'server_list': server_list})

def item_sales(request):
    if request.method == 'POST':
        form = ServerDateRangeForm(request.POST)
        if form.is_valid():
            server_index = form.cleaned_data['server_index']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            return render(request, 'dashboard/compare.html', {'form': form, 'date1': start_date.strftime("%Y-%m-%d"), 'date2': end_date.strftime("%Y-%m-%d")})
    else:
        form = ServerDateRangeForm()
    data = Revenue.get_item_sales()
    dataset = []
    labels = []
    server_list = Revenue.get_server_list()
    for entry in data:
        dataset.append(entry['id__count'])
        labels.append(entry['pay_money'])

    return render(request, 'dashboard/item_sales.html', {"form": form, 'dataset': dataset, 'labels': labels, "server_list": server_list})

class ItemSalesChart(BaseLineChartView):
    def get_data(self):
        start_date = None
        end_date = None
        server_index = None

        try:
            start_date = datetime.strptime(self.kwargs['start_date'], '%Y%m%d')
            end_date = datetime.strptime(self.kwargs['end_date'], '%Y%m%d')
            server_index = self.kwargs['server_index']
        except:
            print("No date range and server selected, getting all data accross servers.")

        query = Revenue.get_item_sales(start_date=start_date, end_date=end_date, server_index=server_index)
        data = []
        for entry in query:
            data.append(entry['id__count'])
        return data
    
    def get_labels(self):
        query = Revenue.get_item_sales()
        labels = []
        for entry in query:
            labels.append(entry['pay_money'])
        return labels

    def get_datasets(self):
        datasets = []
        color_generator = next_color()
        data = self.get_data()
        labels = self.get_labels()
        for item, sales in zip(labels, data):
            color = next(color_generator)
            dataset = {'backgroundColor': color,
                       'label': item,
                       'value': sales}
            datasets.append(dataset)
        datasets = [
            {
                'backgroundColor': COLORS,
                'data': data,
            }
        ]
        return datasets
    def get_colors(self):
        return next_color()

    def get_context_data(self, **kwargs):
        context = {'labels': self.get_labels(), 'datasets': self.get_datasets()}
        return context
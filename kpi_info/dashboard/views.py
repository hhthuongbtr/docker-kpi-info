from django.shortcuts import render
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineOptionsChartView

def dashboard(request):
    return render(request, 'dashboard/index.html')

COLORS = [
    (202, 201, 197),  # Light gray
    (171, 9, 0),      # Red
    (166, 78, 46),    # Light orange
    (255, 190, 67),   # Yellow
    (163, 191, 63),   # Light green
    (122, 159, 191),  # Light blue
    (140, 5, 84),     # Pink
    (166, 133, 93),   # Light brown
    (75, 64, 191),    # Red blue
    (237, 124, 60),    # orange
]

def next_color(color_list=COLORS):
    step = 0
    while True:
        for color in color_list:
            yield list(map(lambda base: (base + step) % 256, color))
        step += 197

class ChartJSONView(BaseLineOptionsChartView): # BaseLineOptionsChartView already inherits
                                               # BaseLineChartView, ChartJSONView just inherits
                                               # from BaseLineOptionsChartView
    def get_labels(self):
        return list(range(0, 23))

    def get_providers(self):
        return ["31/06/2019", "01/07/2019"]

    def get_datasets(self):
        datasets = []
        color_generator = self.get_colors()
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, entry in enumerate(data):
            color = tuple(next(color_generator))
            dataset = {'backgroundColor': "rgba(%d, %d, %d, 0.5)" % color,
                       'borderColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointBackgroundColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointBorderColor': "#fff",
                       'data': entry}
            if i < num:
                dataset['label'] = providers[i]  # series labels for Chart.js
            if i % 2 == 1:
                dataset['type'] = "line"
            datasets.append(dataset)
        return datasets

    def get_data(self):
        return [[18208, 2278, 19117, 3187, 20025, 20934, 5004, 21843, 5913, 22751, 6821, 23660, 7730, 24568, 25477, 9547, 26386, 10456, 27294, 11365, 28203, 12273, 29111, 13182, 25052], 
                [6280, 23119, 7189, 24027, 8097, 24936, 25844, 9915, 26753, 10823, 11732, 28570, 12641, 29479, 13549, 30387, 14458, 31296, 15366, 32205, 16275, 345, 17184, 1254, 19484],
                [28938, 13008, 29846, 13917, 30755, 14825, 31663, 15734, 32572, 16642, 713, 17551, 1621, 18460, 2530, 19368, 3439, 20277, 4347, 21185, 5256, 22094, 6164, 23003, 26212],
                [26405, 10476, 27314, 11384, 28223, 12293, 29131, 13202, 30040, 14110, 30948, 15019, 31857, 15927, 32766, 16836, 906, 17745, 1815, 18653, 2724, 19562, 3632, 20470, 22771],]

    def get_colors(self):
        return next_color()

    def get_options(self):
        return {"scales": {"xAxes": [{"stacked": True}],"yAxes": [{"stacked": True}]}}

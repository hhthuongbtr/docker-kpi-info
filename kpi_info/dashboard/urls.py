from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/chart-json', views.LineChartJSONView.as_view(), name='chart-json')
]

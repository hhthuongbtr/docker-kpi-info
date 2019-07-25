from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/chart-json', views.ChartJSONView.as_view(), name='chart-json')
]

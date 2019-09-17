from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('top_users/', views.top_users, name='top_users'),
    path('api/chart-json/', views.ChartJSONView.as_view(), name='chart-json'),
    path('api/chart-json/<str:date1>/<str:date2>', views.ChartJSONView.as_view(), name='chart-json-compare')
]
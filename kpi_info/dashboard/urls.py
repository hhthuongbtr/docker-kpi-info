from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('top_users/', views.top_users, name='top_users'),
    path('item_sales/', views.item_sales, name='item_sales'),
    path('api/chart-json/', views.ChartJSONView.as_view(), name='chart-json'),
    path('api/chart-json/<str:date1>/<str:date2>', views.ChartJSONView.as_view(), name='chart-json-compare'),
    path('api/chart-json/item_sales', views.ItemSalesChart.as_view(), name='item_sales'),
    path('api/chart-json/<str:date1>-<str:date2>-<str:server>', views.ItemSalesChart.as_view(), name='item_sales_args'),
]

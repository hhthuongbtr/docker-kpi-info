from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('top_users/', views.top_users, name='top_users'),
    path('top_users/<str:start_date>-<str:end_date>-<str:server_index>', views.top_users_update, name='top_users_update'),
    path('item_sales/', views.item_sales, name='item_sales'),
    path('api/chart-json', views.ChartJSONView.as_view(), name='chart-json'),
    path('api/chart-json/<str:date1>/<str:date2>', views.ChartJSONView.as_view(), name='chart-json-compare'),
    path('api/item_sales/', views.ItemSalesChart.as_view(), name='item_sales'),
    path('api/item_sales/<str:start_date>-<str:end_date>-<str:server_index>', views.ItemSalesChart.as_view(), name='item_sales_args'),
]

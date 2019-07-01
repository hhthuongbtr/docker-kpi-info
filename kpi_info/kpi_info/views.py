from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {"customers": 10})

def get_data(request, *args, **kwargs):
    data = {
        "game": 'test',
        "players": 100,
    }
    return JsonResponse(data)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["Games", "Boom", "Khu Vuon Tren May", "Tien Kiem", "AutoChess", "PUBG"]
        default_items = [34, 23, 15, 19, 41, 30]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)


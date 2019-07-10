from django.shortcuts import render

def index(request):
    username = request.user.username
    context = {
        'username': username
    }
    return render(request, 'dashboard/base.html')

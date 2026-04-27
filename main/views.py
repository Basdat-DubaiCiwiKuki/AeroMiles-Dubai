from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html', {'role': 'guest'})

def dashboard(request):
    return render(request, 'dashboard.html', {'role': 'member'})

def identitas(request):
    return render(request, 'identitas.html', {'role': 'member'})
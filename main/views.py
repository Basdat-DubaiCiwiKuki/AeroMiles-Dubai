from django.shortcuts import render, redirect

def login_page(request):
    return render(request, 'login.html', {'role': 'guest'})

def dashboard(request):
    return render(request, 'dashboard.html', {'role': 'member'})

def identitas(request):
    return render(request, 'identitas.html', {'role': 'member'})

def register(request):
    return render(request, 'register.html', {'role': 'guest'})

def profil(request):
    role = request.session.get('role', None)
    if not role:
        return redirect('login')
    return render(request, 'profil.html', {'role': role})
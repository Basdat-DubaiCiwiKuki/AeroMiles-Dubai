from django.shortcuts import render, redirect

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Simulasi login - hardcoded dummy accounts
        if email == 'john@example.com' and password == 'password':
            request.session['role'] = 'member'
            request.session['email'] = email
            request.session['nama'] = 'Mr. John William Doe'
            return redirect('dashboard')
        elif email == 'admin@aeromiles.com' and password == 'password':
            request.session['role'] = 'staf'
            request.session['email'] = email
            request.session['nama'] = 'Mr. Admin Aero'
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'role': 'guest',
                'error': 'Email atau password salah!'
            })
    
    return render(request, 'login.html', {'role': 'guest'})

def dashboard(request):
    role = request.session.get('role', None)
    if not role:
        return redirect('login')
    if role == 'staf':
        return render(request, 'dashboard_staf.html', {'role': 'staf'})
    return render(request, 'dashboard.html', {'role': 'member'})

def logout(request):
    request.session.flush()
    return redirect('login')

def register(request):
    return render(request, 'register.html', {'role': 'guest'})

def identitas(request):
    role = request.session.get('role', None)
    if not role:
        return redirect('login')
    return render(request, 'identitas.html', {'role': 'member'})

def dashboard_staf(request):
    role = request.session.get('role', None)
    if not role:
        return redirect('login')
    return render(request, 'dashboard_staf.html', {'role': 'staf'})
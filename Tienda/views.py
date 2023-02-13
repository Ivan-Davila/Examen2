from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'Tienda/home.html')


def perfil(request):
    pass



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            # Muestra un mensaje de error si los credenciales no son válidos
            return render(request, 'login.html', {'error_message': 'Datos incorrectos'})
    return render(request,'Tienda/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
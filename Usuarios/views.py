from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.
@login_required(login_url='login/')
def home(request):
    return render(request,'home.html')

@login_required
def nuevo_registro(request):
    usuario = request.user
    if usuario.perfilusuario.user_type != 'administrador':
        return render(request,'home.html',{'error_message': 'No tienes permiso para acceder a esta funcion'})
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        tipo_usuario = "distribuidor"
        


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
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def registro(request):
    return redirect('home')

@login_required
def perfil(request):
    pass
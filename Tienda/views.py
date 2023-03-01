from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from Usuarios.forms import LoginForm
# Create your views here.

def home(request):
    return render(request,'Tienda/home.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Recupera los datos del formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Autentica al usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Inicia sesión y redirige al usuario a la página deseada
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'El nombre de usuario o la contraseña son incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'Tienda/login.html', {'form': form})

"""
def login_user(request):
    if request.method == 'POST':
        username = request.POST['correo']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            # Muestra un mensaje de error si los credenciales no son válidos
            return render(request, 'Tienda/login.html', {'error_message': 'Datos incorrectos'})
    return render(request,'Tienda/login.html')"""

def logout_user(request):
    logout(request)
    return redirect('home')
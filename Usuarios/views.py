import re
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Usuarios.models import PerfilUsuario
from validate_email_address import validate_email


# Create your views here.  

@login_required
def nuevo_registro(request):
    usuario = request.user
    if usuario.perfilusuario.user_type != 'administrador' or usuario.perfilusuario.user_type != 'distribuidor':
        return render(request,'home.html',{'error_message': 'No tienes permiso para acceder a esta funcion'})
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        tipo_usuario = "distribuidor"
        
def listar(request):
    users = User.objects.select_related('PerfilUsuario').all()
    return render(request,'Usuarios/listado.html')

def editar(request):
    pass

def eliminar(request):
    pass

def registro(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        tipo_usuario = request.POST['tipo_usuario']
        credito = request.POST['credito']
        if User.objects.filter(email=correo).exists():    
            return render(request, 'registro.html', {'error_message': 'El correo electrónico ya están en uso'})
        if not re.search("^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{10,}$", password):
            return render(request, 'registro.html', {'error_message': 'La contraseña debe tener al menos 10 caracteres y contener números y caracteres especiales'})
        user = User.objects.create_user(password=password,firs_name=nombre,last_name=apellidos,email=correo)
        perfil= PerfilUsuario(user=user)
        perfil.user_tipe=tipo_usuario
        perfil.credito=credito
        perfil.save()
        return redirect('registro')
    return render(request,'Usuarios/registro.html')

@login_required
def perfilCliente(request):
    pass
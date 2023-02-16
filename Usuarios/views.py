import re
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Usuarios.models import PerfilUsuario
from django.contrib import messages
from validate_email_address import validate_email


# Create your views here.  
       
def listar(request):
    user=request.user 
    if user.perfilusuario.user_type == 'administrador' :
        usuarios = User.objects.select_related('perfilusuario').all()
    elif user.perfilusuario.user_type == 'distribuidor' :
        usuarios = User.objects.select_related('perfilusuario').filter(registra=user)
    
    return render(request,'Usuarios/listado.html',{'usuarios':usuarios})

def editar(request):
    pass

def eliminar(request):
    pass

@login_required(login_url='/login/')
def registro(request):
    user=request.user
    if not user.perfilusuario.user_type == 'cliente':
        if request.method == 'POST':
            registrando=request.user
            registrando=registrando.id
            correo = request.POST['correo']
            username=request.POST['username']
            password = request.POST['password']
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            if user.perfilusuario.user_type == 'administrador' :
                tipo_usuario = 'distribuidor'
            elif user.perfilusuario.user_type == 'distribuidor' :
                tipo_usuario='cliente'
            credito = request.POST['credito']
            if User.objects.filter(email=correo).exists():    
                return render(request, 'Usuarios/registro.html', {'error_message': 'El correo electrónico ya están en uso'})
            if not re.search("^(?=.*[0-9])(?=.*[!@#$%^&*-_.])[a-zA-Z0-9!@#$%^&*]{10,}$", password):
                return render(request, 'Usuarios/registro.html', {'error_message': 'La contraseña debe tener al menos 10 caracteres y contener números y caracteres especiales(!@#$%^&*-_.)'})
            user = User.objects.create_user(username=username,password=password,first_name=nombre,last_name=apellidos,email=correo)
            perfil= PerfilUsuario(user=user)
            perfil.user_type=tipo_usuario
            perfil.creditos=credito
            perfil.registra=registrando
            perfil.save()
            return redirect('registro')
        return render(request,'Usuarios/registro.html')
    else:
        messages.warning(request, "No tienes permiso para registrar nuevos usuarios")
        return redirect('home')


@login_required
def perfilCliente(request):
    pass
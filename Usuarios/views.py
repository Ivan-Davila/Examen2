import re
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Usuarios.models import PerfilUsuario
from django.contrib import messages
from validate_email_address import validate_email


# Create your views here.  
@login_required(login_url='/login/')       
def listar(request):
    user=request.user 
    if user.perfilusuario.user_type == 'administrador' :
        usuarios = User.objects.select_related('perfilusuario').all()
    elif user.perfilusuario.user_type == 'distribuidor' :
        usuarios = User.objects.select_related('perfilusuario').filter(registra=user)
    
    return render(request,'Usuarios/listado.html',{'usuarios':usuarios})

@login_required(login_url='/login/')
def editar(request,id_usuario):
    usuario = User.objects.select_related('perfilusuario').get(id=id_usuario)
    if request.method == 'POST':
        usuario.first_name=request.POST['nombre']
        usuario.last_name=request.POST['apellidos']
        usuario.email=request.POST['correo']
        usuario.username=request.POST['username']
        if request.POST['password']:
            usuario.password=request.POST['password']
        usuario.save()
    return render(request,'Usuarios/editar.html',{'usuario':usuario})

@login_required(login_url='/login/')
def eliminar(request,id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    usuario.delete()
    return redirect('lista')

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
            return redirect('registrar')
        return render(request,'Usuarios/registro.html')
    else:
        messages.warning(request, "No tienes permiso para registrar nuevos usuarios")
        return redirect('home')


@login_required(login_url='/login/')
def perfil(request):
    return render(request,'Usuarios/perfilCliente.html')

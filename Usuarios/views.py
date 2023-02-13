from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



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
    users = User.objects.select_related('userprofile').all()
    return render(request,'Usuarios/listado.html')

def editar(request):
    pass

def eliminar(request):
    pass

def registro(request):
    return render(request,'Usuarios/registro.html')

@login_required
def perfil(request):
    pass
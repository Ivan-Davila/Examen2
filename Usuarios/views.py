import re
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Usuarios.models import PerfilUsuario
from django.contrib import messages
from validate_email_address import validate_email
from openpyxl import Workbook
from django.http import HttpResponse
from django.utils import timezone
import pytz
from django.contrib.auth.decorators import permission_required


# Create your views here.  
@permission_required('app.can_view_users_list')   
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
            credito = request.POST['credito']
            if not validate_email(correo):
                return render(request, 'Usuarios/registro.html', {'error_message': 'El correo electrónico es invalido'})
            if user.perfilusuario.user_type == 'administrador' :
                tipo_usuario = 'distribuidor'
            elif user.perfilusuario.user_type == 'distribuidor' :
                tipo_usuario='cliente'
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

@login_required(login_url='/login/')
def exportar(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'

    workbook = Workbook()

    # Selecciona la hoja activa
    worksheet = workbook.active
    worksheet.title = 'Usuarios'

    # Añade los encabezados
    columns = [
        'ID',
        'Nombre',
        'Apellido',
        'Correo electrónico',
        'Tipo de usuario',
        'Credito',
        'Activo',
        'Fecha de registro'
    ]
    row_num=1
    for col_num, column_title in enumerate(columns,1):
        cell = worksheet.cell(row=row_num,column=col_num)
        cell.value = column_title
    
    #Añade los datos
    users = User.objects.select_related('perfilusuario').all()
    for user in users:
        row_num += 1
        date_joined = user.date_joined.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)
        if user.is_active:
            activo='si'
        else:
            activo='no'
        row = [
            user.id,
            user.first_name,
            user.last_name,
            user.email,
            user.perfilusuario.user_type,
            user.perfilusuario.creditos,
            activo,
            date_joined
        ]
        for col_num, cell_value in enumerate(row,1):
            cell = worksheet.cell(row=row_num,column=col_num)
            cell.value = cell_value
    
    workbook.save(response)
    return response
    


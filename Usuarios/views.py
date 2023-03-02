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
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .forms import RegistroUsuarioForm, perfilForm


# Create your views here.  
@login_required(login_url='/login/')
@permission_required('Usuarios.can_view_users_list', login_url='/')   
def listar(request):
    user=request.user 
    if user.perfilusuario.tipo_usuario == 'A' :
        usuarios = User.objects.select_related('perfilusuario').all()
    elif user.perfilusuario.user_type == 'distribuidor' :
        usuarios = User.objects.select_related('perfilusuario').filter(perfilusuario__registra=user.id)
    
    nombre = request.GET.get('nombre')
    correo = request.GET.get('correo')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    # Filtrar los usuarios en base a los parámetros de búsqueda
    if nombre:
        usuarios = usuarios.filter(Q(first_name__icontains=nombre))
    
    if correo:
        usuarios = usuarios.filter(Q(email__icontains=correo))
    
    if fecha_desde and fecha_hasta:
        usuarios = usuarios.filter(Q(date_joined__gte=fecha_desde) & Q(date_joined__lte=fecha_hasta))


    paginator = Paginator(usuarios,5)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    perm = request.user.has_perm('Usuarios.cambiar_credito')
    context = {
        'page_obj': page_obj,
        'perm': perm,
    }
    return render(request,'Usuarios/listado.html',context)
       

@login_required(login_url='/login/')
@permission_required('Usuarios.can_view_users_list',login_url='/')   
def editar(request,id_usuario):
    usuario = User.objects.select_related('perfilusuario').get(id=id_usuario)
    if usuario.perfilusuario.registra == request.user.id:
        if request.method == 'POST':
            usuario.first_name=request.POST['nombre']
            usuario.last_name=request.POST['apellidos']
            usuario.email=request.POST['correo']
            usuario.username=request.POST['username']
            if request.POST['password']:
                usuario.password=request.POST['password']
            usuario.save()
        return render(request,'Usuarios/editar.html',{'usuario':usuario})
    return render(request, 'Usuarios/listado.html', {'error_message': 'no tienes permiso para editar este usuario.'})

@login_required(login_url='/login/')
@permission_required('Usuarios.can_view_users_list',login_url='/')
def eliminar(request,id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    if usuario.perfilusuario.registra == request.user.id:
        usuario.delete()
    else:
        return render(request, 'Usuarios/listado.html', {'error_message': 'no tienes permiso para eliminar este usuario.'})
    return redirect('lista')

@login_required(login_url='/login/')
@permission_required('Usuarios.can_view_users_list',login_url='/')
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                tipo_usuario = 'A'
            elif request.user.perfilusuario.user_type == 'A' :
                tipo_usuario = 'D'
            elif request.user.perfilusuario.user_type == 'D' :
                tipo_usuario='C'
            user = form.save(request,tipo_usuario)
            return redirect('home')
    else:
        tipo_usuario=request.user.perfilusuario.tipo_usuario
        form = RegistroUsuarioForm()
        if tipo_usuario == 'A' or request.user.is_superuser:
            form.fields.pop('creditos')
    return render(request, 'Usuarios/registroform.html', {'form': form})

"""
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
            if user.is_superuser:
                tipo_usuario == 'administrador'
            elif user.perfilusuario.user_type == 'administrador' :
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
            if user.perfilusuario.user_type == 'distribuidor' or user.perfilusuario.user_type == 'administrador':
                can_view_users_list_permission = Permission.objects.get(codename='can_view_users_list')
                user.user_permissions.add(can_view_users_list_permission)
            return redirect('registrar')
        return render(request,'Usuarios/registro.html')
    else:
        messages.warning(request, "No tienes permiso para registrar nuevos usuarios")
        return redirect('home')
"""

@login_required(login_url='/login/')
def user_detail(request):
    user_profile = PerfilUsuario.objects.get(usuario=request.user)
    form = perfilForm(instance=request.user)
    return render(request, 'Usuarios/perfilForm.html', {'form': form})

@login_required(login_url='/login/')
def perfil(request):
    usuario=request.user
    if request.method == 'POST':
        usuario.first_name=request.POST['nombre']
        usuario.last_name=request.POST['apellidos']
        usuario.email=request.POST['correo']
        usuario.save()
    return render(request,'Usuarios/perfilCliente.html')

def suspender(request):
    usuario_id = request.GET.get('usuario_id')
    if request.GET.get('activo') == 'true':
        activo=1
    else:
        activo=0
    print(usuario_id)
    print(activo)
    usuario = User.objects.get(id=usuario_id)
    print(usuario.first_name)
    usuario.is_active = activo
    usuario.save()
    return JsonResponse({'success': True})

@login_required(login_url='/login/')
@permission_required('Usuarios.can_view_users_list',login_url='/')
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

def get_credits(request):
    user = request.user
    return JsonResponse({'credits': user.perfilusuario.creditos})

@login_required(login_url='/login/')
@permission_required('Usuarios.cambiar_credito', login_url='/')       
def editar_credito(request, cliente_id):
    cliente = get_object_or_404(User, id=cliente_id)
    if request.method == 'POST':
        cliente.perfilusuario.creditos = request.POST['credito']
        cliente.save()
        return render(request, 'Usuarios/editar_credito.html', {'cliente': cliente})
    else:
        return render(request, 'Usuarios/editar_credito.html', {'cliente': cliente})
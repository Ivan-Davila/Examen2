from django.shortcuts import render
from Usuarios.models import PerfilUsuario
from django.contrib.auth.models import User
from django.http import JsonResponse
import requests

# Create your views here.

def creditos(request):
    cliente_id = request.GET.get('cliente_id', None)
    if cliente_id:
        cliente = User.objects.filter(id=cliente_id).first()
        if cliente:
            data = {'id': cliente.id, 'nombre': cliente.first_name, 'credito':cliente.perfilusuario.creditos}
            return JsonResponse(data)
    else:
        clientes=User.objects.all()
        data=[{'id': cliente.id, 'nombre': cliente.first_name, 'credito':cliente.perfilusuario.creditos} for cliente in clientes]
        return JsonResponse(data,safe=False)
    
def dolar(request):
    url=f'https://openexchangerates.org/api/latest.json?app_id=f49367ce44e74779aa12b2511ba7293d&symbols=MXN'
    response = requests.get(url)
    data=response.json()
    data=data["rates"]
    return JsonResponse(data)
from django.urls import path
from . import views
from .views import RegistroUsuarioView, ListarUsuariosView


urlpatterns=[
    path('',views.listar,name='lista'),
    path('registrar/',views.registro_form,name='registrar'),
    path('editar/<int:id_usuario>',views.editar,name='editar'),
    path('eliminar/<int:id_usuario>',views.eliminar,name='eliminar'),
    path('perfil/',views.user_detail,name='perfil'),
    path('exportar/',views.exportar,name='exportar'),
    path('suspender/',views.suspender,name='suspender'),
    path('get-credits/',views.get_credits,name='get_credits'),
    path('editar-credito/<int:cliente_id>',views.editar_credito,name='editar_credito'),
    #Clases
    path('registro/', RegistroUsuarioView.as_view(), name='register'),
    path('lista/', ListarUsuariosView.as_view(), name='listado'),
    

]
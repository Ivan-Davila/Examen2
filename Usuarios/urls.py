from django.urls import path
from . import views
from .views import RegistroUsuarioView, ListarUsuariosView, EditarUsuarioView, PerfilUsuarioView


urlpatterns=[
    path('',views.listar,name='lista-fun'),
    path('registrar/',views.registro_form,name='registrar-fun'),
    path('editar/<int:id_usuario>',views.editar,name='editar-fun'),
    path('eliminar/<int:id_usuario>',views.eliminar,name='eliminar'),
    path('perfil/',views.user_detail,name='perfil-fun'),
    path('exportar/',views.exportar,name='exportar'),
    path('suspender/',views.suspender,name='suspender'),
    path('get-credits/',views.get_credits,name='get_credits'),
    path('editar-credito/<int:cliente_id>',views.editar_credito,name='editar_credito'),
    #Clases
    path('registro-form/', RegistroUsuarioView.as_view(), name='registrar'),
    path('lista-form/', ListarUsuariosView.as_view(), name='lista'),
    path('editar-form/<int:id_usuario>', EditarUsuarioView.as_view(),name='editar'),
    #path('perfil-form/', PerfilUsuarioView.as_view(),name='perfil')

]
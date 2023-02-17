from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.listar,name='lista'),
    path('registrar/',views.registro,name='registrar'),
    path('editar/<int:id_usuario>',views.editar,name='editar'),
    path('eliminar/<int:id_usuario>',views.eliminar,name='eliminar'),
    path('perfil/',views.perfil,name='perfil'),

]
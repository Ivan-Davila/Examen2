from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('registrar/',views.registro,name='registro'),
    path('editar/<int:id_usuario>',views.registro,name='registro'),
    path('eliminar/<int:id_usuario>',views.registro,name='registro'),

]
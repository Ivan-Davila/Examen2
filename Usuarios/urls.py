from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("",views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registro/',views.registro,name='registro'),
]
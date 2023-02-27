from django.urls import path
from API import views

urlpatterns=[
    path('creditos/',views.creditos,name="API_creditos"),
    path('dolar/',views.dolar, name='APIdolar')

]
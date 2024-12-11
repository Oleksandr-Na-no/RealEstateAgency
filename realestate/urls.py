from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('house/<int:id>/', views.house, name='house'),
    path('appointment/', views.appointment, name='appointment'),
    path('realtor/', views.realtor, name='realtor'),
    path('get_realtor_tasks/<int:realtor_id>/', views.get_realtor_tasks, name='get_realtor_tasks'),
]
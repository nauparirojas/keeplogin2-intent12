from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_medicina_view, name='panel_medicina'),
    path('citas/nueva/', views.agendar_cita_view, name='cita_nueva'),
    path('pacientes/nuevo/', views.registrar_paciente_view, name='paciente_nuevo'),
]
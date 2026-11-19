from datetime import date
from django.contrib import admin
from .models import CitaMedica, Medico, Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellidos', 'nombres', 'tipo', 'codigo_uncp', 'edad')
    list_filter = ('tipo',)
    search_fields = ('dni', 'nombres', 'apellidos', 'codigo_uncp')

    @admin.display(description='Edad')
    def edad(self, obj):
        hoy = date.today()
        return hoy.year - obj.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day)
        )


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('cmp', 'apellidos', 'nombres', 'especialidad', 'consultorio')
    list_filter = ('especialidad',)
    search_fields = ('cmp', 'nombres', 'apellidos', 'especialidad')


@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora', 'paciente', 'medico', 'estado')
    list_filter = ('estado', 'fecha', 'medico__especialidad', 'medico')
    search_fields = ('paciente__dni', 'paciente__apellidos', 'medico__apellidos')
    list_select_related = ('paciente', 'medico')
    actions = ['marcar_completadas']

    @admin.action(description='Marcar citas como completadas')
    def marcar_completadas(self, request, queryset):
        queryset.update(estado='completada')
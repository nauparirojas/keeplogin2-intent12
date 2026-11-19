from datetime import date, time
from django import forms
from django.utils.html import escape
from .models import CitaMedica, Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'dni', 'nombres', 'apellidos', 'fecha_nacimiento',
            'tipo', 'codigo_uncp', 'correo', 'alergias'
        ]
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})}

    def clean_dni(self):
        dni = (self.cleaned_data.get('dni') or '').strip()
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError('El DNI debe tener exactamente 8 dígitos numéricos.')
        return dni

    def clean_fecha_nacimiento(self):
        fnac = self.cleaned_data.get('fecha_nacimiento')
        if fnac and fnac > date.today():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
        return fnac

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        correo = (cleaned.get('correo') or '').strip().lower()
        if tipo == 'estudiante' and not correo.endswith('@uncp.edu.pe'):
            self.add_error('correo', 'El correo institucional @uncp.edu.pe es obligatorio para estudiantes.')
        return cleaned


class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'medico', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_motivo(self):
        motivo = escape((self.cleaned_data.get('motivo') or '').strip())
        if len(motivo) < 20:
            raise forms.ValidationError('El motivo de consulta debe tener al menos 20 caracteres.')
        return motivo

    def clean(self):
        cleaned = super().clean()
        paciente = cleaned.get('paciente')
        medico = cleaned.get('medico')
        fecha = cleaned.get('fecha')
        hora = cleaned.get('hora')

        if fecha and hora:
            es_sabado = fecha.weekday() == 5
            es_domingo = fecha.weekday() == 6
            if es_domingo:
                self.add_error('fecha', 'No hay atención médica los domingos.')
            elif es_sabado and not (time(8, 0) <= hora <= time(13, 0)):
                self.add_error('hora', 'Los sábados la atención es de 08:00 a 13:00.')
            elif not es_sabado and not (time(8, 0) <= hora <= time(18, 0)):
                self.add_error('hora', 'De lunes a viernes la atención es de 08:00 a 18:00.')

        if paciente and fecha:
            if CitaMedica.objects.filter(paciente=paciente, fecha=fecha).exclude(estado='cancelada').exists():
                raise forms.ValidationError('El paciente ya tiene una cita registrada en esta fecha.')

        if medico and fecha and hora:
            if CitaMedica.objects.filter(medico=medico, fecha=fecha, hora=hora).exclude(estado='cancelada').exists():
                self.add_error('hora', 'Ese horario ya está ocupado para el médico seleccionado.')

        return cleaned
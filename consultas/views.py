from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CitaMedicaForm, PacienteForm
from .models import CitaMedica, Medico, Paciente


@login_required
def panel_medicina_view(request):
    alerta_citas = request.session.pop('alerta_citas', None)
    citas = CitaMedica.objects.select_related('paciente', 'medico').order_by('fecha', 'hora')
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()
    return render(
        request,
        'consultas/panel.html',
        {
            'citas': citas,
            'medicos': medicos,
            'pacientes': pacientes,
            'alerta_citas': alerta_citas,
        },
    )


@login_required
def agendar_cita_view(request):
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita médica agendada correctamente.')
            return redirect('panel_medicina')
    else:
        form = CitaMedicaForm()
    return render(request, 'consultas/cita_form.html', {'form': form})


@login_required
def registrar_paciente_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente registrado correctamente.')
            return redirect('panel_medicina')
    else:
        form = PacienteForm()
    return render(request, 'consultas/paciente_form.html', {'form': form})
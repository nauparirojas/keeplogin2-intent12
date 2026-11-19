import logging
from django.utils import timezone
from .models import CitaMedica

logger = logging.getLogger('auditoria_medica')


class AuditoriaMedicaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario = request.user.username if request.user.is_authenticated else 'anonimo'

        if request.user.is_authenticated and not request.session.get('aviso_citas_hoy'):
            pendientes = CitaMedica.objects.filter(
                fecha=timezone.localdate(), estado='pendiente'
            ).count()
            if pendientes > 0:
                request.session['alerta_citas'] = f'Hay {pendientes} cita(s) médica(s) pendiente(s) para hoy.'
            request.session['aviso_citas_hoy'] = True

        response = self.get_response(request)

        if 'historial' in request.path or request.method in ('POST', 'PUT', 'DELETE'):
            logger.info(f"MED_AUDIT | user={usuario} | method={request.method} | path={request.path}")

        return response
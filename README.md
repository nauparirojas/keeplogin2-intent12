# Caso 2: Gestión de Consultas Médicas (UNCP)

Aplicación Django independiente para el **Caso 2** de la Práctica Grupal Semana 12 (IS093A):
- Registro de pacientes y médicos con validaciones de DNI (8 dígitos), fecha de nacimiento no futura y correo `@uncp.edu.pe` para estudiantes.
- Agendamiento de citas con validación de horario de atención (L-V 08:00-18:00, Sáb 08:00-13:00), motivo mínimo de 20 caracteres, sin duplicidad diaria por paciente y sin cruce de horario por médico.
- Middleware de auditoría médica, sesión con expiración por inactividad y Django Admin con campos calculados y acción masiva.

## Ejecución
1. `python -m venv venv` y `.\venv\Scripts\Activate`
2. `pip install -r requirements.txt`
3. `python manage.py makemigrations` y `python manage.py migrate`
4. `python manage.py createsuperuser` y `python manage.py runserver`

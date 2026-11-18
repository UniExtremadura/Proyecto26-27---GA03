# Guía de desarrollo

## Puesta en marcha

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py          # http://127.0.0.1:5000
pytest                 # ejecutar las pruebas
```

Usuarios de demostración (datos ficticios): `alumno1`, `alumno2`, `alumno3`, `profesor1`, `profesor2`, `pas1`.
Contraseña de todos: `demo1234`.

## Arquitectura

- `app/__init__.py`: fábrica de la aplicación; descubre automáticamente los módulos de `app/modules`.
- `app/db.py`: SQLite y esquema base (`users`, `asignaturas`, `matriculas`).
- `app/auth.py`: sesión web, token Bearer para las apps (`/api/token`, `/api/yo`).
- `app/registry.py`: cada módulo registra su entrada de menú y su buscador.
- `app/modules/<historia>.py`: una historia de usuario = un módulo + sus plantillas + sus pruebas.

## Convención de ramas y commits

- Una rama por historia: `feature/SCRUM-<n>-us-<nn>-<slug>`, creada desde `main`.
- Un commit por subtarea de Jira; el mensaje empieza por la clave: `SCRUM-98 Diseñar el flujo de matrícula online guiado`.
- Integración en `main` mediante *pull request* (ver plantilla) cuando se cumple la Definition of Done.

## Orden recomendado de integración (dependencias de Jira)

1. Sprint 1: US-15, US-16, US-05
2. Sprint 2: US-14, US-04, US-06, US-07, US-08, US-11
3. Sprint 3: US-01, US-02, US-03
4. Sprint 4: US-09, US-13, US-17
5. Sprint 5: US-10, US-12

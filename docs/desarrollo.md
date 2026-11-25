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

## Flujo de trabajo: GitFlow + Smart Commits de Jira

Ramas:

- `main`: versiones finales. Solo recibe `develop` al cierre del sprint.
- `develop`: integración. **De aquí salen y aquí vuelven todas las ramas de historia.**
- `feature/SCRUM-<n>-<slug>`: una rama por historia de usuario, creada desde `develop` (desde Jira: *Create branch*).

Reglas:

1. Antes de tocar código, pasa la subtarea a **En curso** en Jira.
2. **Un commit y un push por subtarea**, con la clave de la subtarea al principio del mensaje, en una sola línea:

   ```
   SCRUM-98 #time 1h 30m #comment Diseñado el flujo de matrícula en tres pasos #finalizado
   ```

3. Nombres de transición de ESTE proyecto de Jira (los espacios se sustituyen por guiones): `#en-curso`, `#en-revisión`, `#finalizado`. El PDF de la práctica usa `#done`, que aquí **no existe**.
4. Todos los merges con `--no-ff` (una sola vez por repositorio): `git config merge.ff false`.
   Con esa opción usa `git pull --ff-only` para no crear merges al actualizar.
5. Al terminar todas las subtareas de una historia, se integra en `develop` en este orden:

   ```bash
   git checkout feature/SCRUM-24-...
   git pull --ff-only
   git merge --no-ff develop -m "SCRUM-24 #comment Integrados los últimos cambios de develop"
   # resolver conflictos, ejecutar TODAS las pruebas (pytest) y publicar
   git push origin feature/SCRUM-24-...
   git checkout develop && git pull --ff-only
   git merge --no-ff feature/SCRUM-24-... -m "SCRUM-24 #comment Requisito integrado en develop #finalizado"
   git push origin develop
   ```

   No pongas `#time` en los commits de merge. Si trabajas con *pull requests*, elige **Create a merge commit** (nunca Squash ni Rebase).
6. Cierre del sprint: `develop` → `main` con `--no-ff` y el mensaje `Versión final del sprint: todos los requisitos integrados`.

## Orden recomendado de integración (dependencias de Jira)

1. Sprint 1: US-15, US-16, US-05
2. Sprint 2: US-14, US-04, US-06, US-07, US-08, US-11
3. Sprint 3: US-01, US-02, US-03
4. Sprint 4: US-09, US-13, US-17
5. Sprint 5: US-10, US-12

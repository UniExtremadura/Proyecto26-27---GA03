# EP-02: Facilitación de navegación

**Goals:** G-02, G-03, G-06, G-08
**Versión de referencia:** Campus Virtual v1.0

## Límites

### Incluye
- Rediseño de menús.
- Breadcrumbs.
- Buscador global.
- Acceso a información de asignaturas, eventos y servicio CAUX.

### Excluye
- Cambios en la lógica de negocio de los trámites (EP-01).
- Rediseño visual (EP-04).

## Resultado de la épica

Permitir que cualquier usuario encuentre lo que busca en pocos clics mediante una estructura de navegación clara, consistente y con buscador transversal, mejorando también el acceso a la información de asignaturas, eventos y CAUX.

## Historias de usuario

### US-05: Navegación clara e intuitiva

> Como estudiante de la UNEX, quiero que se diseñe una navegación clara, con menús y buscador, para poder encontrar lo que busco lo antes posible.

- **Prioridad:** Must
- **Estimación del esfuerzo:** -1h
- **Incertidumbre:** Baja
- **Predecesores:** Ninguno indicado

#### Criterios de aceptación
- **US-05-AC-01:** Toda página muestra migas de pan.
- **US-05-AC-02:** Existe buscador global accesible desde cualquier pantalla.
- **US-05-AC-03:** Se llega a los servicios principales en máximo 5 clics.

#### Verificaciones y restricciones
- **Verificaciones:** Test de usabilidad con alumnos.
- **Restricciones:** Mantener compatibilidad con URLs existentes en medida de lo posible.

### US-06: Información de la asignatura

> Como estudiante de la UNEX, quiero ver la ficha completa de una asignatura, sus docentes y partes asignadas de la asignatura a cada uno de ellos, para poder elegir las asignaturas a las que me matriculo con información suficiente.

- **Prioridad:** Should
- **Estimación del esfuerzo:** -1h
- **Incertidumbre:** Baja
- **Predecesores:** US-15

#### Criterios de aceptación
- **US-06-AC-01:** La ficha muestra guía docente, horarios, profesor y créditos.
- **US-06-AC-02:** La información se sincroniza con la fuente oficial.
- **US-06-AC-03:** Es accesible sin autenticación.

#### Verificaciones y restricciones
- **Verificaciones:** Comparación con datos del departamento.
- **Restricciones:** Información validada por el departamento responsable.

### US-07: Información de eventos

> Como estudiante de la UNEX, quiero consultar la información de eventos académicos para participar en los que me interesen.

- **Prioridad:** Could
- **Estimación del esfuerzo:** -1h
- **Incertidumbre:** Baja
- **Predecesores:** US-15

#### Criterios de aceptación
- **US-07-AC-01:** Se muestra listado con fecha, lugar e inscripción.
- **US-07-AC-02:** Solo aparecen eventos aprobados por el organizador.
- **US-07-AC-03:** La actualización tarda menos de 30 min desde su publicación.

#### Verificaciones y restricciones
- **Verificaciones:** Prueba de publicación y refresco.
- **Restricciones:** Fuente de eventos centralizada.

### US-08: Mejora del servicio CAUX

> Como estudiante de la UNEX, quiero resolver dudas con CAUX desde el campus, para no tener necesidad de llamar o desplazarme.

- **Prioridad:** Could
- **Estimación del esfuerzo:** 1-3h
- **Incertidumbre:** Media
- **Predecesores:** US-05

#### Criterios de aceptación
- **US-08-AC-01:** Se puede pedir cita previa online.
- **US-08-AC-02:** Existe FAQ con buscador.
- **US-08-AC-03:** La confirmación de cita llega en menos de 10s.

#### Verificaciones y restricciones
- **Verificaciones:** Integración con el sistema de citas existente.
- **Restricciones:** Horarios y disponibilidad del personal.
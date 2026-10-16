# EP-05: Mejora de administración técnica

**Goals:** G-01, G-04, G-06, G-07, G-08
**Versión de referencia:** Campus Virtual v1.0

## Límites

### Incluye
- Estabilidad.
- Persistencia ante fallos.
- Integración Outlook.
- Rediseño y gestión de BD.

### Excluye
- Cambios visibles de diseño.
- Nuevos trámites funcionales.

## Resultado de la épica

Dotar al campus de una base técnica estable, segura y eficiente (alta disponibilidad, persistencia, integración Outlook y BD optimizada) que soporte sin incidencias el resto de épicas.

## Historias de usuario

### US-14: Protección contra fallos o pérdidas de conexión

> Como usuario de la UNEX, quiero que mi progreso durante un trámite no se vea interrumpido por un fallo de la web o por una pérdida de conexión, para no tener que rellenar un formulario largo varias veces.

- **Prioridad:** Must
- **Estimación del esfuerzo:** 8+h
- **Incertidumbre:** Alta
- **Predecesores:** US-15, US-16

#### Criterios de aceptación
- **US-14-AC-01:** Autoguardado cada cambio de campo.
- **US-14-AC-02:** Al reabrir se ofrece recuperar el borrador.
- **US-14-AC-03:** Indicador visual "Guardado" / "Sin guardar".

#### Verificaciones y restricciones
- **Verificaciones:** Prueba de corte de red y cierre inesperado.
- **Restricciones:** Los borradores caducan a los 30 días.

### US-15: Mejora de la base de datos y su gestión

> Como administrador de la UNEX, quiero una base de datos robusta, que no provoque fallos, para que el campus funcione sin errores y se eviten las pérdidas de datos.

- **Prioridad:** Must
- **Estimación del esfuerzo:** 8+h
- **Incertidumbre:** Alta
- **Predecesores:** Ninguno indicado

#### Criterios de aceptación
- **US-15-AC-01:** Migración sin pérdida de datos.
- **US-15-AC-02:** Backups automáticos diarios.
- **US-15-AC-03:** Consultas críticas en menos de 1 s.

#### Verificaciones y restricciones
- **Verificaciones:** Simulacro de restauración de backup.
- **Restricciones:** Ventanas de mantenimiento y compatibilidad con sistemas actuales.

### US-16: Mejoría de la estabilidad del servicio

> Como usuario de la UNEX, quiero que el campus esté disponible y sea estable, para poder usarlo cuando lo necesite.

- **Prioridad:** Must
- **Estimación del esfuerzo:** 8+h
- **Incertidumbre:** Alta
- **Predecesores:** Ninguno indicado

#### Criterios de aceptación
- **US-16-AC-01:** Disponibilidad ≥99,5 % mensual.
- **US-16-AC-02:** Monitorización con alertas ante caídas.
- **US-16-AC-03:** Recuperación automática ante fallo de un nodo.

#### Verificaciones y restricciones
- **Verificaciones:** Prueba de caos y simulación de fallo de nodo.
- **Restricciones:** RTO <1 h y RPO <15 min.

### US-17: Integración de Outlook dentro del campus

> Como usuario de la UNEX, quiero ver mi correo de Outlook dentro del campus, para no tener que cambiar de aplicación/pestaña.

- **Prioridad:** Could
- **Estimación del esfuerzo:** 8+h
- **Incertidumbre:** Alta
- **Predecesores:** US-15, US-16

#### Criterios de aceptación
- **US-17-AC-01:** Login SSO con cuenta institucional.
- **US-17-AC-02:** Vista de calendario y eventos.
- **US-17-AC-03:** Sincronización en menos de 5 min.

#### Verificaciones y restricciones
- **Verificaciones:** Prueba con API de Microsoft y permisos TI.
- **Restricciones:** Cumplimiento de políticas de seguridad.
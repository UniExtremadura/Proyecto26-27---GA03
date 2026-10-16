# EP-01: Simplificación de trámites

**Goals:** G-02, G-03, G-04
**Versión de referencia:** Campus Virtual v1.0

## Límites

### Incluye
- Matrícula.
- Desmatriculación.
- Solicitud de becas.
- Descarga de documentos oficiales (matrícula, expediente).

### Excluye
- Trámites con firma notarial.
- Convalidaciones externas.
- Pagos con pasarelas no integradas.

## Resultado de la épica

Digitalizar y unificar los trámites académicos clave en un flujo online guiado, reduciendo tiempo, desplazamientos y errores del alumno, permitiendo además monitorizar el estado de cada solicitud.

## Historias de usuario

### US-01: Alumno quiere matricularse

> Como estudiante de la UNEX, quiero matricularme de forma sencilla e intuitiva, para no tener que hacerlo presencialmente y tener una validación instantánea.

- **Prioridad:** Must
- **Estimación del esfuerzo:** 5-8h
- **Incertidumbre:** Baja
- **Predecesores:** US-05, US-14, US-15, US-16

#### Criterios de aceptación
- **US-01-AC-01:** El alumno puede seleccionar asignaturas de su plan de estudios.
- **US-01-AC-02:** El sistema valida prerrequisitos, plazas y solapamientos antes de confirmar.
- **US-01-AC-03:** Se genera un justificante de matrícula descargable en PDF.

#### Verificaciones y restricciones
- **Verificaciones:** Pruebas de integración con el sistema de expedientes.
- **Restricciones:** Solo disponible en el periodo oficial de matrícula.

### US-02: Alumno quiere desmatricularse

> Como estudiante de la UNEX, quiero desmatricularme de forma sencilla e intuitiva, para no tener que hacerlo presencialmente y tener una validación instantánea.

- **Prioridad:** Must
- **Estimación del esfuerzo:** 5-8h
- **Incertidumbre:** Baja
- **Predecesores:** US-05, US-14, US-15, US-16

#### Criterios de aceptación
- **US-02-AC-01:** El alumno puede seleccionar una asignatura matriculada y solicitar su anulación.
- **US-02-AC-02:** El expediente y el recibo se actualizan automáticamente.
- **US-02-AC-03:** El sistema bloquea la operación fuera de plazo con mensaje explicativo.

#### Verificaciones y restricciones
- **Verificaciones:** Casos de prueba con fechas límite.
- **Restricciones:** Solo disponible en el periodo oficial de matrícula.

### US-03: Alumno quiere pedir una beca y poder monitorizar su estado en vivo

> Como estudiante de la UNEX, quiero poder monitorizar el progreso en la concesión de cualquier beca en proceso, así como mayor facilidad en el trámite, para saber si falta documentación o está resuelta.

- **Prioridad:** Must
- **Estimación del esfuerzo:** 3-5h
- **Incertidumbre:** Media
- **Predecesores:** US-04, US-14, US-15

#### Criterios de aceptación
- **US-03-AC-01:** El formulario permite adjuntar la documentación requerida.
- **US-03-AC-02:** El estado se muestra como Solicitada / En revisión / Falta documentación / Aprobada / Denegada.
- **US-03-AC-03:** El alumno recibe notificación al cambiar de estado.

#### Verificaciones y restricciones
- **Verificaciones:** Prueba con lector de pantalla (accesibilidad).
- **Restricciones:** Sujeto a las bases reguladoras de la convocatoria.

### US-04: Descarga de documentos oficiales

> Como estudiante de la UNEX, quiero poder descargar mi matrícula, expediente o cualquier otro documento para no tener la necesidad de solicitarlo de forma presencial.

- **Prioridad:** Should
- **Estimación del esfuerzo:** 1-3h
- **Incertidumbre:** Baja
- **Predecesores:** US-15

#### Criterios de aceptación
- **US-04-AC-01:** El alumno puede ver un listado de sus documentos disponibles.
- **US-04-AC-02:** La descarga se realiza en PDF firmado.
- **US-04-AC-03:** Solo el titular (y los que se ocupen de la gestión de estos) puede acceder a sus documentos.

#### Verificaciones y restricciones
- **Verificaciones:** Prueba de descargas. Prueba de acceso con usuario ajeno (debe denegar).
- **Restricciones:** Formato de descarga y firma según normativa académica.
# EP-04: Cambio de diseño

**Goals:** G-02, G-03, G-04
**Versión de referencia:** Campus Virtual v1.0

## Límites

### Incluye
- Guía de estilo.
- Rediseño estético.
- Directorio de perfiles.
- Apps de escritorio y móvil.

### Excluye
- Cambios en lógica de trámites.
- Cambios en la base de datos.

## Resultado de la épica

Renovar la identidad visual y la experiencia de usuario, ofreciendo una interfaz moderna y coherente, y extendiendo el acceso mediante apps de escritorio y móvil.

## Historias de usuario

### HU-10: Campus más estético

> Como estudiante de la UNEX, quiero un campus visiblemente agradable, para que pueda usarlo a gusto.

- **Prioridad:** Won't
- **Estimación del esfuerzo:** 1-3h
- **Incertidumbre:** Baja
- **Predecesores:** US-05

#### Criterios de aceptación
- **US-10-AC-01:** Se aplica una nueva guía de estilo consistente.
- **US-10-AC-02:** El contraste cumple WCAG AA.
- **US-10-AC-03:** El diseño es responsive.

#### Verificaciones y restricciones
- **Verificaciones:** Revisión con imagen corporativa.
- **Restricciones:** Sin romper accesibilidad ni funcionalidad.

### HU-11: Directorio de perfiles

> Como usuario de la UNEX, quiero poder encontrar el perfil y contacto de un alumno o profesor de la UNEX para poder contactar con él.

- **Prioridad:** Should
- **Estimación del esfuerzo:** -1h
- **Incertidumbre:** Baja
- **Predecesores:** US-05, US-15

#### Criterios de aceptación
- **US-11-AC-01:** Búsqueda por nombre, departamento o asignatura.
- **US-11-AC-02:** Solo se muestra información pública autorizada.
- **US-11-AC-03:** Los resultados en menos de 2 s.

#### Verificaciones y restricciones
- **Verificaciones:** Prueba de acceso a datos sensibles.
- **Restricciones:** No exponer datos sensibles sin consentimiento previo.

### HU-12: App de escritorio

> Como usuario de la UNEX, quiero una aplicación de escritorio para poder acceder al campus y su información más rápido y sin usar el navegador.

- **Prioridad:** Won't
- **Estimación del esfuerzo:** 5-8h
- **Incertidumbre:** Alta
- **Predecesores:** US-15, US-16

#### Criterios de aceptación
- **US-12-AC-01:** Instalable en Windows y macOS.
- **US-12-AC-02:** Login y accesos clave funcionan.
- **US-12-AC-03:** Funcionamiento similar o mejor al campus en navegador.

#### Verificaciones y restricciones
- **Verificaciones:** Pruebas de usuarios.
- **Restricciones:** Multiplataforma y actualizaciones automáticas.

### HU-13: App de móvil

> Como usuario de la UNEX, quiero una aplicación de móvil para poder acceder al campus cuando no tenga acceso a mi ordenador.

- **Prioridad:** Could
- **Estimación del esfuerzo:** 5-8h
- **Incertidumbre:** Alta
- **Predecesores:** US-15, US-16

#### Criterios de aceptación
- **US-13-AC-01:** Diseño responsive en Android y iOS.
- **US-13-AC-02:** Login y accesos clave funcionan.
- **US-13-AC-03:** Funcionamiento similar al campus en navegador.

#### Verificaciones y restricciones
- **Verificaciones:** Publicación en stores y pruebas en dispositivos reales.
- **Restricciones:** Mismas validaciones que la web.
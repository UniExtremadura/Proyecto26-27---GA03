# Goals.md — Proyecto de Reestructuración y Mejora del Campus Virtual, Portal de Alumnos y Webs Institucionales de la UNEX

# 1. Propósito del documento
Este documento transforma la dirección estratégica establecida en la misión del proyecto en resultados concretos, medibles y alcanzables. Constituye la fuente de referencia oficial para la definición de objetivos, indicadores de éxito, límites de alcance, exclusiones, supuestos y restricciones del proyecto de reestructuración y mejora del Campus Virtual, el Portal de Alumnos, sus servicios asociados y las distintas webs de la Universidad de Extremadura (UNEX).

# 2. Objetivos
## 2.1 Objetivo general
Modernizar, unificar y optimizar la plataforma digital de la UNEX para ofrecer una experiencia de usuario coherente, accesible, segura y eficiente, alineada con las necesidades de estudiantes, profesorado y personal de administración y servicios (PAS).

## 2.2 Objetivos específicos
N.º	Objetivo	Definición
G-01	Renovar la arquitectura del Campus Virtual	Migrar/actualizar la plataforma a una versión soportada y escalable, con integración nativa con los sistemas corporativos.
G-02	Rediseñar el Portal de Alumnos	Implementar una interfaz centrada en el usuario que unifique trámites académicos, consultas y servicios.
G-03	Unificar la imagen y experiencia de las webs UNEX	Aplicar un sistema de diseño común a todas las webs institucionales.
G-04	Actualizar los servicios digitales asociados	Renovar APIs, autenticación (SSO), notificaciones y servicios de integración.
G-05	Garantizar accesibilidad y cumplimiento normativo	Alcanzar conformidad WCAG 2.1 AA y normativa europea de accesibilidad y protección de datos
G-06	Mejorar el rendimiento y la disponibilidad	Reducir tiempos de carga y garantizar alta disponibilidad de los servicios críticos.
G-07	Fortalecer la seguridad de la información	Aplicar medidas de seguridad alineadas con ENS (Esquema Nacional de Seguridad) y RGPD.
G-08	Habilitar la gestión y publicación autónoma de contenidos	Dotar al personal de herramientas y formación para gestionar contenidos sin dependencia técnica.

# 3. Indicadores y criterios de éxito
N.º	Indicador	Métrica	Método de comprobación	Objetivo
M-01	Satisfacción de estudiantes y profesores	Encuesta NPS/CSAT	Encuesta post-implantación	≥ 4/5
M-02	Tiempo de carga (LCP)	Core Web Vitals	Lighthouse / RUM	≤ 2,5 s
M-03	Accesibilidad	Conformidad WCAG 2.1 AA	Auditoría externa	100% (pág. críticas)
M-04	Disponibilidad de servicios	Uptime mensual	Monitorización (Zabbix)	≥ 99,5%
M-05	Adopción del nuevo Portal	%usuarios activos mensuales	Analítica web	≥ 85% del alumnado
M-06	Reducción de incidencias	Tickets de soporte	Sistema de tickets	-50%
M-07	Cobertura de migración de webs	N.º de webs migradas	Inventario de webs	100%
M-08	Cobertura de tests automatizados	%código cubierto	CI/CD	≥ 70% (mod. críticos)
M-09	Formación al personal	%PAS/profesorado formado	| Registro de formación	≥ 90%

# 4. Límites del alcance
## 4.1 Incluido
- I-01: Rediseño y migración del Campus Virtual (LMS) a versión soportada.
- I-02: Rediseño funcional y visual del Portal de Alumnos.
- I-03: Actualización de servicios asociados: SSO, APIs, notificaciones, integraciones con SGA (Sistema de Gestión Académica).
- I-04: Migración y unificación de las webs institucionales de la UNEX a un sistema de diseño común.
- I-05: Implementación de accesibilidad WCAG 2.1 AA.
- I-06: Mejoras de seguridad alineadas con ENS y RGPD.
- I-07: Formación y documentación para el personal.
- I-08: Plan de comunicación y gestión del cambio.

# 5. Exclusiones
- EX-01: Reingeniería de procesos administrativos de secretaría.
- EX-02: Renovación de infraestructura física de red o servidores salvo la necesaria para el despliegue.
- EX-03: Integración con plataformas de terceros no aprobadas previamente por el comité.
- EX-04: Traducción de contenidos a idiomas distintos de español.
- EX-05: Desarrollo de nuevas titulaciones o modificación de planes de estudio.
- EX-06: Cambios en los procesos administrativos internos (solo su digitalización).
- EX-07: Renovación del hardware de los centros o aulas.
- EX-08: Sistemas de gestión económica o de RRHH (excepto integraciones puntuales).

# 6. Supuestos
- S-01: Existe disponibilidad presupuestaria aprobada para todo el ciclo del proyecto.
- S-02: La dirección de la UNEX mantiene el compromiso y patrocinio del proyecto.
- S-03: El personal clave (PAS, profesorado, alumnado) participará en las fases de validación.
- S-04: Los proveedores externos cumplirán los plazos y estándares acordados.
- S-05: La infraestructura cloud/on-premise estará disponible y dimensionada según lo previsto.
- S-06: Los sistemas corporativos exponen APIs utilizables.
- S-07: La normativa vigente (RGPD, ENS, accesibilidad) no sufrirá cambios sustanciales durante el proyecto.
- S-08: Los usuarios finales dispondrán de conectividad y dispositivos adecuados.

# 7. Restricciones
Tipo	Restricción
Tiempo	El proyecto debe completarse en un plazo máximo de 6 meses.
Presupuesto	Ejecución dentro del presupuesto asignado, sin ampliaciones no aprobadas.
Legal	Cumplimiento obligatorio de RGPD, LOPDGDD, ENS y normativa de accesibilidad (RD 1112/2018).
Técnica	Compatibilidad con sistemas corporativos existentes y con los navegadores soportados.
Recursos	Equipo interno limitado; dependencia de proveedores externos para desarrollo e integración.
Organizativa	No se pueden interrumpir los servicios durante los periodos lectivos críticos (matrícula, exámenes).
Idiomática	Contenidos en español (e inglés de forma ocasional).
Seguridad	Cualquier despliegue debe superar auditoría de seguridad previa a producción.


# 8. Criterios de aceptación global
El proyecto se considerará exitoso cuando:
1. Todos los objetivos específicos (OE1–OE8) se hayan cumplido y validado.
2. Los indicadores de la sección 3 alcancen los valores objetivo.
3. Se haya superado la auditoría de accesibilidad, seguridad y rendimiento.
4. El personal haya sido formado y los manuales entregados.
5. Los servicios antiguos hayan sido desmantelados sin pérdida de datos ni de servicio.
6. La satisfacción global de los usuarios sea igual o superior a los umbrales definidos.

# 9. Revisión y gobernanza
Este documento será revisado al inicio de cada fase del proyecto. Cualquier cambio en objetivos, alcance o restricciones deberá ser aprobado por el Comité de Dirección del Proyecto. 
Versión: 1.0 — Fecha de aprobación: [pendiente].
Responsable: [Dirección del Proyecto / Oficina de Transformación Digital UNEX].

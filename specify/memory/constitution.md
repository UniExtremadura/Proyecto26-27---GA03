Este documento define los principios fundamentales, normas de gobierno y criterios de calidad que deberán respetarse 
durante todo el proyecto de remodelación de la plataforma digital de la Universidad de Extremadura.

No define funcionalidades concretas ni decisiones de implementación. Su objetivo es establecer las reglas que deberán cumplir las especificaciones, 
planes, desarrollos, pruebas y decisiones que se realicen durante el proyecto.

# Principios fundamentales

## 1. Especificación y trazabilidad

Toda funcionalidad deberá estar especificada antes de ser implementada.
Las dependencias funcionales, técnicas y externas deberán identificarse durante la especificación y quedar documentadas en la definición de los requisitos.
Cada funcionalidad deberá responder a una necesidad previamente identificada y deberá mantenerse una relación trazable entre:

Necesidad → Requisito → Criterio de aceptación → Plan → Tarea → Implementación → Prueba

Los elementos del proyecto utilizarán identificadores estables:

Épicas: EP-XXX
Historias de usuario: US-XXX
Tareas: TK-XXX
Subtareas: ST-XXXX
Iteraciones: IT-XXX

Estos identificadores deberán mantenerse de forma consistente en los diferentes artefactos y herramientas de gestión utilizadas por el proyecto.

No deberán implementarse funcionalidades que no puedan relacionarse con un requisito aprobado.

## 2. Disciplina de alcance
El proyecto deberá centrarse en las funcionalidades necesarias para conseguir remodelar la página web a una plataforma más útil, estable, accesible y mantenible.

Las ampliaciones de alcance deberán:

- Estar justificada.
- Tener una prioridad definida mediante MoSCoW (Must, Should, Could, Won't).
- Justificar la prioridad considerando el valor, el riesgo y las dependencias.
- Evaluar su impacto en tiempo, coste y cantidad.
- Identificar dependencias y riesgos.
- Quedar documentada.

Cualquier modificación que afecte a objetivos, alcance, exclusiones, supuestos, restricciones o métricas deberá ser revisada por el equipo, aprobada mediante el procedimiento de gestión de cambios establecido y reflejada en los artefactos afectados.

## 3. Calidad y comportamiento verificable
Una funcionalidad deberá funcionar correctamente ante situaciones previsibles.
La calidad deberá considerarse parte del producto y no una actividad posterior al desarrollo.
Cada funcionalidad debe incluir:

- Criterios de aceptación.
- Casos de error.
- Estados vacíos.
- Estados de carga.
- Casos límite.

## 4. Seguridad, privacidad y protección de datos
La seguridad deberá considerarse desde la especificación hasta la implementación y las pruebas.
La solución deberá aplicar principios como:
- Autorización explícita.
- Gestión segura de sesiones.
- Protección de información sensible.
- Control adecuado de permisos.
- Gestión segura de errores.

Durante su desarrollo se utilizarán preferentemente datos ficticios.
No deberán incluirse datos personales reales en:
- Repositorios.
- Ejemplos.
- Capturas de pantalla públicas.
- Documentación técnica pública.
- Datos de demostración.

Cualquier tratamiento de datos reales deberá estar justificado y autorizado.

## 5. Usabilidad y accesibilidad
La plataforma deberá ser comprensible, consistente y fácil de utilizar.
La accesibilidad será un requisito transversal del proyecto.
Los flujos principales deberán diseñarse teniendo en cuenta:
- Diversidad de usuarios.
- Uso mediante teclado.
- Tecnologías de asistencia.
- Contraste.
- Legibilidad.
- Jerarquía visual.
- Mensajes de error comprensibles.
- Formularios accesibles.
- Diseño adaptable.
- Claridad del lenguaje.
  
Los componentes deberán mantener patrones consistentes en toda la plataforma.

## 6.Compatibilidad e interoperabilidad
La remodelación deberá tener en cuenta las dependencias existentes con otros sistemas.
Antes de modificar una integración deberán identificarse:
- Sistema afectado.
- Datos intercambiados.
- Dependencias.
- Riesgos.
- Compatibilidad.
  
No deberá romperse deliberadamente una integración existente sin una estrategia explícita de sustitución o transición.
Los cambios incompatibles deberán estar claramente identificados y justificados.

## 7. Definition of Ready
Una historia de usuario podrá entrar en planificación y desarrollo únicamente cuando cumpla el Definition of Ready establecida por el equipo.

El Definition of Ready deberá comprobar, cuando corresponda, que la historia dispone de identificación, trazabilidad, usuario o stakeholder, alcance, criterios de aceptación, prioridad, estimación, incertidumbre, dependencias, requisitos no funcionales, restricciones y cuestiones abiertas suficientemente resueltas.

## 8. Definition of Done
Una funcionalidad se considerará terminada únicamente cuando:
- El código esté implementado conforme a la arquitectura y convenciones acordadas.
- Cumpla los criterios de aceptación.
- Las pruebas necesarias sean satisfactorias.
- Los errores previsibles estén tratados.
- La funcionalidad haya sido integrada correctamente.
- La documentación y trazabilidad necesarias estén actualizadas.
- Cumpla, como norma general, todo lo que esta definido en este documento



`constitution.md`
Define los principios, normas y criterios de gobierno del proyecto.
No deberá definir funcionalidades concretas ni detalles técnicos específicos salvo cuando sean necesarios.

`spec.md`
Define qué se necesita y por qué.

Deberá incluir, cuando corresponda:

- Problema.
- Contexto.
- Objetivos.
- Usuarios.
- Requisitos.
- Restricciones.

`plan.md`
Define cómo se abordará técnicamente una especificación aprobada.
Podrá incluir:
- Arquitectura.
- Componentes.
- Integraciones.
- Modelo de datos.
- Seguridad.
- Decisiones de implementación.

`tasks.md`
Descompone el plan en trabajo concreto y ejecutable.
Cada tarea deberá:
- Tener un objetivo claro.
- Producir un resultado verificable.
- Referenciar los requisitos afectados.

# Gobierno

## 1. Jerarquia

El orden de autoridad documental será:

1. `constitution.md`

2. Especificaciones aprobadas.

3. Decisiones de arquitectura aprobadas.

4. `plan.md`

5. `tasks.md`

6. Documentación de implementación.

Ningún documento de nivel inferior podrá superponerse a uno superior.

## 2. Versionado

Este documento seguirá versionado semántico:

MAJOR.MINOR.PATCH

MAJOR

Cambios que alteran principios fundamentales, autoridad o normas obligatorias.

Ejemplo:

1.0.0 → 2.0.0

MINOR

Incorporación de nuevos principios o ampliaciones relevantes que no invalidan los existentes.

Ejemplo:

1.1.0 → 1.2.0

PATCH

Aclaraciones, correcciones o mejoras de redacción que no modifican el significado normativo.

Ejemplo:

1.0.0 → 1.0.1

## 3. Modificación y excepciones

Cualquier miembro del equipo podrá proponer una modificación de esta constitución.

Toda modificación deberá estar justificada, ser aprobada por todos los miembros del equipo y registrar:

- Versión.
- Fecha.
- Motivo del cambio.
- Documentos o decisiones afectados.

Las excepciones a esta constitución deberán estar justificadas, aprobadas por el equipo y documentadas. Cuando sea posible, tendrán carácter temporal y deberán indicar la condición o momento en que dejarán de aplicarse.

## Historial de versiones

Versión: 1.1.0

Fecha : 03/10/2026

Descripción: Redacción del `constituión.md`


  

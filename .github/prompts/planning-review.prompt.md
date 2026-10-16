---
name: Planning Review
description: "Ejecuta una revisión de planificación inicial con Planning Agent usando datos y fuentes concretas del equipo."
argument-hint: "Indica baseline, objetivo, IDs, plan, estimaciones, capacidad, dependencias y restricciones."
agent: "Planning Agent"
tools: [read, search]
---
Revisa la planificación inicial con Planning Agent. Usa los siguientes datos para esta ejecución:

- **Baseline:** ${input:baseline:Indica versión, fecha, commit o artefacto que fija la baseline}
- **Plan y asignación inicial:** ${input:plan:Indica la ruta del plan y el sprint asignado a cada requisito o ID}
- **Objetivo, entrega, IDs y prioridades:** ${input:scope:Indica el objetivo, entrega prevista, requisitos incluidos y prioridades aprobadas}
- **Estimaciones:** ${input:estimates:Indica la fuente, unidad, responsable y alcance cubierto por cada estimación}
- **Capacidad efectiva:** ${input:capacity:Indica disponibilidad por persona y semana, ausencias, coordinación y otras deducciones}
- **Dependencias y capacidades del equipo:** ${input:dependencies:Indica dependencias por resultado, su estado y las capacidades necesarias/disponibles}
- **Horizonte, hitos y restricciones:** ${input:horizon:Indica semanas o sprints, hitos, fechas límite y restricciones aplicables}
- **Costes y presupuesto:** ${input:costs:Indica tarifas, presupuesto disponible, alcance y cobertura de costes}
- **Supuestos e incertidumbre:** ${input:assumptions:Indica supuestos materiales, responsable o rol y momento previsto de validación}
- **Margen:** ${input:margin:Define si es margen de tiempo, capacidad, presupuesto u otro; aporta método, datos y evidencia, o indica «sin definir»}

Consulta las fuentes indicadas sin modificarlas. La duración de cada sprint de la asignatura es de una semana. Si un campo no está disponible, no inventes su contenido: solicita los datos materiales que falten o limita explícitamente la evaluación a lo que sí pueda comprobarse.

Evalúa, según los datos disponibles:
1. Que el plan identifique objetivo, entrega e IDs; señala propuestas de ampliar, aplazar o reducir alcance e indica su efecto esperado, sin decidirlas.
2. La cobertura y procedencia de estimaciones, incluidas unidad, responsable y trabajo cubierto.
3. La capacidad efectiva por persona y semana, descontando ausencias, coordinación y otras deducciones declaradas.
4. El horizonte, la carga, el roadmap, la duración semanal de los sprints y si alguna historia parece excesiva respecto de la capacidad declarada.
5. La secuencia de requisitos por sprint, sus dependencias y el estado de las capacidades necesarias; comprueba si la planificación inicial es compatible con estos datos y el tiempo de desarrollo.
6. La presencia y viabilidad de hitos, costes, tarifas, presupuesto, restricciones, supuestos e incertidumbres.

No inventes estimaciones, velocidad histórica ni factores de conversión. Si el equipo propone un factor de conversión, regístralo como modelo declarado y supuesto cuya validez requiere evidencia. No supongas qué significa «margen» si no se define.

Devuelve el informe en la conversación, sin editar ni replanificar archivos. Incluye baseline, objetivo, entrega, IDs y fuentes revisadas; hallazgos por dimensión; datos y unidades usados en cada cálculo; distinción entre evidencia, cálculo, supuesto y pregunta abierta; efectos esperados de las alternativas de alcance; limitaciones; y datos que el equipo debe aportar o validar. No presentes un plan alternativo como aplicado.
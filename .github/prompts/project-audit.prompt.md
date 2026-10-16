---
name: Project Audit
description: "Ejecuta una auditoría de riesgos, cronograma y recursos de ProjectLibre con Agente Auditor, usando una baseline y fuentes concretas."
argument-hint: "Indica baseline, archivo o exportación de ProjectLibre, riesgos, requisitos, recursos y criterios de coste y margen."
agent: "Agente Auditor"
tools: [read, search]
---
Audita los riesgos y la planificación registrada en ProjectLibre con Agente Auditor. Usa estos datos para esta ejecución:

- **Baseline y periodo:** ${input:baseline:Indica versión, fecha, commit y periodo que representa el plan}
- **Archivo o exportación de ProjectLibre:** ${input:projectFile:Indica la ruta del archivo del proyecto o de una exportación legible como XML, CSV, hoja de cálculo o PDF}
- **Objetivo, alcance e IDs:** ${input:scope:Indica objetivo, entrega, IDs de requisitos/tareas incluidos y fuentes de alcance}
- **Registro de riesgos:** ${input:risks:Indica la ruta del registro o describe riesgos con situación, evento, consecuencia y tratamiento}
- **Calendario y recursos:** ${input:calendarResources:Indica las fuentes del calendario laboral, recursos, disponibilidad/capacidad, ausencias y tarifas}
- **Tareas, estimaciones y asignaciones:** ${input:tasksAssignments:Indica dónde constan IDs, estimación, unidad, esfuerzo, duración, predecesores y asignaciones de recursos}
- **Costes y restricciones:** ${input:costsConstraints:Indica presupuesto, reglas de coste, restricciones y fuentes de autoridad}
- **Métodos y criterios acordados:** ${input:criteria:Indica escalas de riesgo, criterios de camino crítico y reglas para holgura, margen y reservas; si no están definidos, escribe «sin definir»}

Consulta las fuentes indicadas sin modificarlas. Si el archivo de ProjectLibre no se puede leer directamente, solicita una exportación legible con los campos necesarios. Si faltan baseline, cronograma o datos materiales, pregunta por ellos o limita explícitamente la auditoría; no inventes rutas, cifras ni métodos.

Evalúa, según la evidencia disponible:
1. Riesgos del proyecto, incluyendo situación o causa, evento, consecuencia y tratamiento previsto; distingue riesgos de problemas ocurridos.
2. Integridad del ProjectLibre: calendario, recursos con capacidad y coste, tareas con IDs/estimación/esfuerzo/duración, dependencias y asignaciones coherentes con el esfuerzo.
3. Viabilidad de asignaciones: capacidad efectiva por persona y periodo, carga, sobreasignaciones, esfuerzo, duración, disponibilidad, tarifas y coste real de las asignaciones.
4. Viabilidad de la secuencia de requisitos: orden y paralelización, dependencias, competencias, hitos, camino crítico, holguras, margen y reservas.

Muestra unidades, datos de origen y fórmulas para los cálculos. Separa evidencia directa, cálculo, supuesto, inferencia y dato ausente. No inventes escalas de riesgo, calendarios, disponibilidades, tarifas ni reglas de margen; no trates holgura, margen y reserva como equivalentes sin una definición acordada.

Devuelve el informe en la conversación, sin editar archivos ni replanificar. Incluye baseline, fuentes y alcance auditado; hallazgos por dimensión con referencias e impacto; datos no disponibles y limitaciones; y preguntas o recomendaciones para el equipo. No declares el plan viable o inviable sin criterios explícitos y evidencia suficiente.
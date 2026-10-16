---
name: Requirements Review
description: "Ejecuta una revisión versionada de una baseline concreta del catálogo de requisitos usando Requirements Reviewer."
argument-hint: "Indica baseline, rutas de requisitos, ámbito y destino del informe."
agent: "Requirements Reviewer"
tools: [read, search, edit]
---
Ejecuta una revisión de requisitos con Requirements Reviewer. Usa los siguientes datos para esta ejecución:

- **Baseline:** ${input:baseline:Indica versión, fecha, commit o artefacto que fija la baseline}
- **Catálogo y requisitos detallados:** ${input:requirements:Indica las rutas reales del catálogo y de las historias o requisitos incluidos}
- **Requisitos o historias diferidas:** ${input:deferred:Indica las rutas que deben considerarse diferidas, o escribe «ninguno»}
- **Ámbito y contexto:** ${input:scope:Indica las rutas de visión, objetivos, alcance e idea del equipo; incluye stakeholders si están en fuentes separadas}
- **Fuentes de calidad:** ${input:quality:Indica las rutas vigentes del DoR y DoD; si no se indican, búscalas en el workspace y documenta si no existen}
- **Carpeta de informes:** ${input:reportPath:Indica la ruta workspace-relativa donde guardar el informe}
- **Versión nueva:** ${input:version:Indica un identificador de versión nuevo para este informe}

Lee las fuentes indicadas sin modificarlas. Si no se proporcionan una baseline, los requisitos concretos, el ámbito o el destino del informe, pide la información que falte antes de continuar; no inventes rutas ni alcance.

Evalúa, como mínimo, estas dimensiones:
1. Claridad, consistencia y verificabilidad de requisitos funcionales y no funcionales; detecta ambigüedades, duplicidades y contradicciones.
2. Cobertura de requisitos respecto a objetivos y stakeholders, posibles omisiones y propuestas fuera del alcance documentado.
3. Tamaño y granularidad de historias; usa INVEST como heurística. No separes en historias las tareas de backend, frontend o pruebas solo por capa técnica.
4. Suficiencia y observabilidad de criterios de aceptación, incluidos estados vacíos y casos límite pertinentes.
5. Cumplimiento del DoR común de equipo y distinción respecto del DoD, que define la calidad del incremento terminado.
6. Dependencias y supuestos no identificados.

Incluye también requisitos no funcionales, restricciones, reglas de negocio y casos límite ausentes en las dimensiones pertinentes. Comprueba cualquier propuesta de funcionalidad frente a la visión, el alcance y la idea del equipo; deja sin resolver lo que no esté respaldado por las fuentes.

Escribe un **informe Markdown nuevo** en la carpeta indicada, usando el identificador de versión proporcionado. Antes de escribir, comprueba si el destino ya existe; no sobrescribas archivos. Si el nombre está ocupado, usa un nombre libre con un sufijo incremental y registra el nombre elegido. No edites ninguna fuente ni generes una versión revisada del catálogo.

Organiza el informe por dimensiones. Para cada hallazgo incluye referencia, evidencia, problema, impacto, propuesta de mejora y pregunta o decisión pendiente si aplica. Registra baseline, rutas revisadas, ámbito incluido/excluido y limitaciones. No clasifiques ni priorices recomendaciones; el equipo las clasificará y decidirá cuáles incorporar al catálogo revisado.
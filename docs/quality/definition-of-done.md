# Definition of Done (DoD)
Una historia de usuario se considerará como realizada cuando se cumpla con las siguientes condiciones
## Implementación

- La funcionalidad descrita en las historias de usuario ha sido implementada.
- La implementación respeta la arquitectura y principios definidos para el proyecto.
- No quedan problemas críticos de implementación por resolver.
- La funcionalidad se comporta correctamente en los escenarios previstos.
  
## Criterios de aceptación

- Todos los criterios de aceptación asociados a las historias de usuario han sido verificados.
- El comportamiento implementado coincide con la historia de usuario asociada a ella.
- Existen pruebas de la verificación cuando sea necesaria.
- Los casos de error y situaciones límite definidas han sido comprobadas.

## Pruebas
- Se han ejecutado las pruebas necesarias.
- Las pruebas cubren el comportamiento esperado.
- Se han comprobado las condiciones de error importantes.
- Las pruebas existentes relacionadas siguen siendo satisfactorias.
- No se han detectado regresiones críticas conocidas.

## Integración
- La implementación se ha integrado en la rama o entorno acordado para el proyecto.
- La versión integrada compila, se ejecuta y funciona correctamente.
- La funcionalidad se integra correctamente con los componentes o servicios de los que depende.
- El cambio no introduce incompatibilidades críticas conocidas con otras partes de la plataforma.

## Requisitos no funcionales
- Se han comprobado los requisitos no funcionales.
- Se han considerado los requisitos de seguridad correspondientes.
- Se han considerado los requisitos de privacidad y protección de datos.
- Se ha comprobado la usabilidad.
- Se ha comprobado la accesibilidad.
- Se ha verificado el comportamiento en los dispositivos y tamaños de pantalla.
- Se han considerado los requisitos de rendimiento cuando sean relevantes.

## Documentación y trazabilidad
- La documentación técnica ha sido actualizada.
- La documentación dirigida al usuario ha sido actualizada.
- La historia de usuario puede relacionarse con su implementación y con las pruebas que verifican su comportamiento.
- Las decisiones tomadas durante la implementación han quedado documentadas.

Se mantiene la trazabilidad:

Necesidad → Requisito → Historia de usuario → Implementación → Pruebas → Validación

## Revisión
- El trabajo ha sido revisado siguiendo el proceso acordado por el equipo.
- Los problemas detectados durante la revisión han sido resueltos o aceptados.
- No quedan incidencias ni defectos críticos conocidos.
- La implementación cumple los principios establecidos en `constitution.md`.

## Validación final
Antes de considerar una Historia de usuario terminada deberá poder responder a las siguientes preguntas:
- ¿La funcionalidad está completamente implementada?
- ¿Cumple todos sus criterios de aceptación?
- ¿Ha sido probada correctamente?
- ¿Los errores están tratados?
- ¿Se integra correctamente con el resto del proyecto?
- ¿Se han comprobado seguridad, privacidad, accesibilidad y usabilidad?
- ¿Se han evitado regresiones?
- ¿La documentación está actualizada?
- ¿Existe trazabilidad entre la necesidad y el resultado?
- ¿El trabajo ha sido revisado?
- ¿Cumple `constitution.md`?

Si alguna condición obligatoria no se cumple, la Historia de usuario no podrá considerarse realizada.

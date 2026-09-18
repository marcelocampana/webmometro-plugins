# Cierre de una tarea que aprueba o publica contenido

**Condicional.** Una tarea de código, de configuración o de análisis no llega aquí: solo se lee cuando
lo que cierra la tarea es la **aprobación o publicación de una pieza de contenido** —un artículo, una
página—. Su archivo fuente lleva un `estado:` en el frontmatter que hay que mover en el mismo cierre: `borrador` → `en-revision` → `aprobado` → `validado` → `publicado`. Si no se
actualiza ahí, el archivo queda mintiendo sobre su propio estado y cualquier verificación posterior
parte de un dato falso (`content-sync-check` solo compara lo aprobado).

**`validado` no es un `aprobado` más fuerte: es otra cosa.** `aprobado` dice que la redacción está
cerrada; `validado` dice que un equipo externo —médico, legal— revisó **una versión concreta**, que
queda congelada con su hash. Solo se entra ahí cuando el usuario lo dice explícitamente. (No lo
confundas con los estados de la *tarea*, que son otros y viven en `estados.md`.)

**Va dentro de la cadena de cierre, no como paso aparte**: sin una segunda pregunta, igual que el
archivado. Tres movimientos, el último condicional:

1. **Actualiza `estado:`** al valor que corresponda y **`fecha_aprobacion:`** con la fecha del
   cierre (de `date '+%Y-%m-%d'`, nunca inventada). Si el archivo no tiene esos campos, añádelos.
2. **Dilo en la misma línea de cierre**: qué archivo y a qué estado pasó.
3. **Si el estado que corresponde es `validado`, no lo escribas a mano**: invoca
   `content-sync-check` (su `references/validacion.md`, no una de aquí) o corre `sellar_validacion.py <fuente>
   --validado-por "<quién>"`. Escribir `estado: validado` sin la copia congelada y sin
   `hash_validado` deja el archivo afirmando un ancla que no existe — peor que no tenerla, porque
   la verificación posterior confía en ella.

**Si la tarea modifica una pieza que ya estaba en `validado`**, el cierre **no** la deja ahí: la
baja a `en-revision` y lo dice. La validación caducó con el cambio, y dejarla marcada como validada
haría pasar por revisado algo que nadie revisó.

**Es condicional y no se fuerza.** Una tarea de código, de configuración o de análisis no toca
ningún `estado:`. Si no está claro qué pieza aprueba la tarea —o si toca varias—, **pregunta cuáles
antes de escribir**: es la única excepción que añade una pregunta, y solo cuando la respuesta no
está en la tarea.

La fuente es el archivo del workspace de contenido (`web/contenido/**`), **nunca la copia del repo
del sitio ni la del proyecto de diseño**: esas son destinos y se alimentan de la fuente.

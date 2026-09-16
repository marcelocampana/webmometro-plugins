# Impacto documental (después del merge)

Se lee **con la cadena de cierre ya terminada**, nunca antes: nada queda a medias si el usuario no
contesta. Dos tiempos — detectar barato, y solo entonces leer.

1. **Detectar.** Del diff de la rama (`git diff --name-only main@{1}...`), busca señales de que la
   documentación pudo quedar corta: cambió la estructura de directorios; se añadió, renombró o
   eliminó un archivo que el README enumera, un comando, un script, una dependencia o una variable de
   entorno; o se tocó algo que `CLAUDE.md` describe como convención, layout o invariante. **Sin señal,
   silencio total**: no lo menciones ni digas que lo miraste.

2. **Verificar, solo lo señalado.** Abre **únicamente** los archivos que la señal apunta —nunca el
   directorio de documentación entero—: el README y los archivos que enlaza, `CLAUDE.md`, y de `docs/`
   solo el que cubre el área tocada. Comprueba si la afirmación concreta sigue siendo cierta. **Si
   sigue al día, silencio**: haber leído no obliga a decir nada.

3. **Decir lo que sepas, y solo eso.** Con una discrepancia verificada, **una línea**: qué archivo,
   qué afirma hoy y qué dice el repo, con las dos salidas en la misma pregunta. Si el paso 2 no pudo
   concluir —archivo demasiado grande, afirmación ambigua—, di la sospecha sin resolverla y ofrece
   solo `revisar.md`. **No redactes el reemplazo** en ninguno de los dos casos: el diagnóstico es la
   entrega.

> Cerrada y mergeada. `docs/skills.md` lista 3 skills en utils y ahora son 4: falta
> `content-sync-check`. ¿Lo anoto en `revisar.md` o lo corrijo ahora?

Si el usuario dice «corrígelo», es **una tarea nueva y corta** —rama, commit y merge propios—, no una
extensión de la que acaba de cerrarse: esa cadena ya terminó. Esto **no es un cuarto freno**: ocurre
con el merge hecho, así que nada queda a medias si el usuario no contesta.

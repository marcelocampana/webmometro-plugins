# El comparador: qué hace el script y qué te toca a ti

La comparación tiene dos capas y hacen cosas distintas. **El script dice dónde difiere; tú dices
qué significa.** Confundirlas degrada las dos: si interpretas sin correr el script, se te escapa
una negación; si reportas su salida cruda, entierras al usuario en diferencias sin jerarquía.

## Invocar

```bash
python3 "<ruta-del-skill>/scripts/comparar_contenido.py" <fuente> <destino>
python3 "<ruta-del-skill>/scripts/comparar_contenido.py" <fuente> <destino> --modo estricto
python3 "<ruta-del-skill>/scripts/comparar_contenido.py" <fuente> "Portada.dc.html" --variante movil
python3 "<ruta-del-skill>/scripts/comparar_contenido.py" --auditar-mapeo contexto/configuracion.md --raiz <raíz>
```

Devuelve JSON. Códigos: `0` sin diferencias · `1` hay diferencias · `2` error de lectura o parseo.
**`2` nunca significa "coincide"** — significa que no se comparó nada.

El script **no llama a `DesignSync`**: recibe rutas y ya. Consigue tú el `.dc.html` antes (del
espejo local, de un export, o escribiéndolo al scratchpad desde `DesignSync get_file`) y pásale la
ruta. Si no sabes de dónde debe salir, pregunta: la respuesta cambia contra qué estás comparando.

## Leer la salida

**Mira `veredicto` primero.** Decide si hay algo que interpretar:

| `veredicto` | Qué haces |
| --- | --- |
| `identico` | Nada. Reportas "coincide" en una línea y paras. |
| `identico_reordenado` | Solo evalúas si el reorden cambia el sentido. Nada más. |
| `difiere` | Interpretas **los bloques listados**, no la página entera. |
| cualquiera con `--modo estricto` | Manda el script. Todo bloquea (`validacion.md`). |

Los campos que vas a usar: `diferencias` (pares con las dos versiones literales),
`solo_en_fuente` (no llegó al destino), `solo_en_destino` (**nadie lo aprobó** — prioridad alta),
`reubicaciones` (mismo texto, otro bloque), `orden.movidos`, `marcadores_pendiente`,
`notas_internas_en_destino` (contenido interno filtrado: siempre hallazgo) y `avisos`.

**No vuelques el JSON al usuario.** Es insumo interno; lo que él ve es el reporte de
`verificacion.md`.

## Por qué casi siempre hay algo que interpretar

Un texto que el diseño **movió** aparece en el diff como dos diferencias: eliminación aquí,
inserción allá. El script es ciego a la reubicación por diseño — por eso existe el paso que la
detecta, y por eso su campo `reubicaciones` ya hizo esa comprobación. Lo que se ahorra con
`identico` es el caso limpio, que en verificaciones rutinarias es frecuente.

## Cómo se reporta

**Marca la procedencia de cada hallazgo.** «El script encontró que estas dos cifras difieren» tiene
otra certeza que «creo que este reorden cambia el sentido»; en un listado plano las dos se leen con
la misma autoridad, y eso es engañoso.

- `⚠` **verificado** — lo detectó el script. Diferencia literal, con las dos versiones citadas. No
  admite discusión: está o no está.
- `?` **interpretado** — lo aportas tú. Una reubicación, un juicio sobre el reorden, clasificar algo
  como solo forma. Va con su razón en la misma línea.

Los `⚠` primero. **Cifras, fechas, fármacos y fuentes citadas en su propio grupo**, sin mezclar con
diferencias de redacción (`reconciliacion.md`). El texto se cita literal, nunca se parafrasea.

## Las dos normalizaciones

El script trae dos y **no son intercambiables**:

- `texto_visible` / `normalizar_estricta` — **para verificar**. Preserva tildes, mayúsculas y
  cifras: `mama` ≠ `mamá`, `5.333` ≠ `5,333`. Solo absorbe lo que nadie lee: entidades HTML,
  comillas y guiones tipográficos, espaciado, énfasis Markdown y marcadores `[PENDIENTE-…]`.
- `normalizar_difusa` — **solo para emparejar** texto movido. Descarta tildes, caja y puntuación.

`dispositivos.md` normaliza sin tildes ni mayúsculas: **es la difusa**, y sirve para *buscar* texto
entre variantes, nunca para decidir que dos textos coinciden. Bajo ella `mamá` y `mama` son
iguales — y eso, en contenido clínico, es exactamente lo que no puede pasar al verificar.

## Qué queda fuera del chequeo

`--auditar-mapeo` no compara: diagnostica. Devuelve `fuera_del_chequeo` (piezas mapeadas que se
saltan, casi siempre por no tener `estado:`), `rutas_rotas` y `avisos`.

**Repórtalo en el resumen, no al final.** Una pieza sin `estado:` se salta en silencio: el reporte
sale limpio y parece completo sin serlo. Decir «3 de 5 páginas no se verificaron» es más útil que
cualquier hallazgo de las otras dos. Ofrece añadir el `estado:` que falte (lo pone `task-flow` al
aprobar); no lo escribas por tu cuenta.

## Si el script no corre

**Dilo en una línea, con el error, y compara leyendo** con las reglas de `comparacion.md`. Un
chequeo leído vale; uno que calla que el script no corrió, no.

| Situación | Qué hacer |
| --- | --- |
| No hay `python3`, o el script falla | Dilo con el error y compara leyendo. No lo intentes en bucle. |
| Sale código `2` | No se comparó nada. **Nunca lo reportes como coincidencia.** |
| Un `.dc.html` grande devuelve menos de ~20 bloques | El aviso lo señala: es extracción fallida, no página vacía. No concluyas que falta contenido. |
| `avisos` menciona constantes ignoradas | Normal (estilos, estado de interfaz). Solo míralo si falta contenido que esperabas. |
| El formato detectado no es el que esperabas | Fuérzalo con `--formato-fuente` / `--formato-destino` y vuelve a correr. |

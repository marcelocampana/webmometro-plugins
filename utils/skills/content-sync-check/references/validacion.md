# El ancla de validación: qué revisó el equipo médico

`estado: aprobado` dice que la redacción está cerrada. **No dice qué versión revisó nadie.** Si la
fuente se corrige después de la revisión médica, una verificación de sincronía diría "todo en orden"
contra una fuente que ya no es la validada — y el chequeo estaría confirmando lo que no debe.

El ancla cierra ese hueco: congela una copia del contenido revisado, guarda su huella, y permite
comprobar si la fuente sigue siendo esa.

## `validado` no es un `aprobado` más fuerte

Son cosas distintas. `aprobado` es una decisión editorial interna. `validado` dice que **un equipo
externo revisó una versión concreta**, que quedó congelada. Solo se entra a `validado` cuando el
usuario lo dice explícitamente; no se deduce de que una tarea se cerró.

## Los cinco campos

```yaml
estado: validado
validado_por: "Dra. X, Observatorio del Cáncer"
fecha_validacion: 2026-09-05
hash_validado: "sha256:9f2c1a…"
copia_validada: ".validado/cancer-de-mama-hub-copy.2026-09-05.md"
```

**Nunca los escribas a mano.** Un `estado: validado` sin copia congelada ni hash deja el archivo
afirmando un ancla que no existe, y es peor que no tenerla: la verificación posterior confía en ella.

## La copia congelada

Vive en `.validado/` junto al archivo fuente, con la fecha en el nombre:
`web/contenido/clusters/.validado/<pieza>.<AAAA-MM-DD>.md`

- **Empieza por punto** porque el workspace es un vault de Obsidian: sin el punto, cada copia
  aparecería en el grafo, la búsqueda y el autocompletado, duplicando cada página del clúster.
- **Lleva fecha** porque una pieza puede revalidarse tras una corrección médica. Con nombre fijo, la
  segunda validación borraría la evidencia de la primera; el historial de qué se revisó y cuándo es
  parte de lo que se protege. La más reciente es la vigente; `copia_validada` apunta a ella.
- **No se edita a mano.** Es la única evidencia de qué se revisó.

## Qué mide el hash

El texto comparable de la pieza, con la **misma normalización que usa el diff**. En consecuencia:

- Reordenar claves del frontmatter, cambiar comillas rectas por tipográficas o que iCloud reescriba
  los saltos de línea **no** rompe el ancla. Un ancla que grita en falso deja de creerse, y a la
  tercera vez nadie la mira.
- Cambiar una cifra, una negación o una palabra **sí** la rompe.
- Mover un bloque de prosa **sí** la rompe: contra la versión validada, moverse es una diferencia.
- La metadata de proceso queda fuera (si no, escribir el hash cambiaría el hash).

**Hashes de formatos distintos nunca coinciden.** Un `.md` y un `.dc.html` producen huellas
distintas aunque digan lo mismo. Contra el canvas el ancla es el diff en `--modo estricto`, no la
igualdad de hash: no esperes que cuadren.

## Los comandos

```bash
python3 "<ruta-del-skill>/scripts/sellar_validacion.py" <fuente.md> --mostrar
python3 "<ruta-del-skill>/scripts/sellar_validacion.py" <fuente.md> --verificar
python3 "<ruta-del-skill>/scripts/sellar_validacion.py" <fuente.md> --validado-por "<quién>"
```

Solo `--validado-por` escribe. Códigos: `0` en orden · `1` la fuente cambió tras validarse · `2`
error. Tras sellar, el script relee y comprueba: el vault vive en iCloud, y una escritura que no
sincronizó se parece mucho a una que falló.

## El flujo

1. La pieza está en `estado: aprobado`.
2. El equipo médico revisa. El usuario lo comunica.
3. **Antes de sellar**, compara en `--modo estricto` contra cada destino declarado. Congelar una
   versión que ya diverge de lo publicado consagra la divergencia. Si hay diferencias, se resuelven
   primero.
4. Con el visto bueno, `--validado-por "<quién>"`.
5. **En cada corrida posterior**, `--verificar` como parte del Paso 0.
6. **Antes de publicar**, la pregunta que justifica todo esto se responde así:
   `comparar_contenido.py <copia_validada> <destino> --modo estricto`. `identico` con el orden
   intacto es la única respuesta que autoriza.

## La excepción dura

**Contra la versión validada, el diff manda solo.** En `--modo estricto` cualquier diferencia pone
`bloquea_publicacion: true` — incluidas las reubicaciones y el reorden. Contra lo que alguien
revisó, «solo se movió» no atenúa nada.

Tu juicio sirve para decidir **qué hacer** con la diferencia. Nunca para decidir que la diferencia
es aceptable.

## Qué hacer con un bloqueo

**No lo trates como un hallazgo más y no ofrezcas reparar.** Reparar propaga la fuente a los
destinos; ante una diferencia contra la copia validada, la fuente puede ser justamente la que se
desvió, y propagarla esparciría el problema en vez de resolverlo.

Repórtalo **antes que cualquier otro hallazgo**, con las versiones literales, y presenta las dos
únicas salidas legítimas:

1. **Revalidar** — el contenido nuevo es correcto y el equipo debe revisarlo. Se sella una
   validación nueva; la anterior queda como registro.
2. **Revertir** — la copia congelada gobierna. Se restaura desde ella y se propaga.

Si el usuario no decide ahora, regístralo como tarea con las versiones literales (`task-flow`); no
dejes la decisión solo en el chat. **Mientras el bloqueo esté en pie, ninguna pieza se declara
sincronizada ni lista para publicar.**

## Cuando una pieza validada se modifica

Corregir la fuente de una pieza en `estado: validado` **invalida la validación**. Dilo en el momento
y ofrece resellar. Si la corrección la cierra `task-flow`, el estado baja a `en-revision`
(`task-flow/references/archivado.md`): la validación caducó con el cambio.

## Errores

| Situación | Qué hacer |
| --- | --- |
| `veredicto: sin_validar` | La pieza no tiene ancla. Dilo: no se puede afirmar que coincida con nada revisado. Ofrece sellar si el equipo ya revisó. |
| `veredicto: copia_ausente` | Hay hash pero falta la copia congelada. Declara que no se puede mostrar qué se validó; no lo trates como coincidencia. |
| `estado: validado` sin `hash_validado` | Alguien lo escribió a mano. El ancla no existe: dilo y ofrece sellar de verdad. |
| La copia congelada se editó a mano | Se perdió la evidencia. Dilo con claridad; la única salida es revalidar con el equipo. |
| El usuario pide sellar sin haber comparado antes | Compara primero (paso 3). Sellar sobre una divergencia desconocida la convierte en oficial. |

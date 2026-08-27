# Cómo sacar el texto de una página de diseño

Una página `.dc.html` **no guarda su texto en el marcado**. Lo guarda en constantes de un script y
lo renderiza con plantillas (`sc-for`, `{{ item.q }}`). Quien busque el texto leyendo el HTML
visible encontrará `{{ item.q }}` y concluirá que el contenido no está — y dará por ausente lo que
sí existe. **Es el error más fácil de cometer aquí, y produce hallazgos falsos en contenido
médico.**

Comprobado en las páginas reales de un proyecto: todas usan este patrón, con entre 4 y 12
constantes de datos por página. No es un caso excepcional; es cómo están hechas.

## El método, en orden

**1 · Localiza las constantes de datos.** Son arrays al inicio del script, con nombres semánticos:

```
const faqs = [...]        const treatments = [...]    const impact = [...]
const videos = [...]      const challenges = [...]    const toc = [...]
```

Búscalas con `const <nombre> = [`. Da igual el nombre exacto —cambia por página—: lo que importa es
que un array de objetos con texto es contenido.

**2 · Extrae el texto de cada array.** Los valores van entre comillas simples con escapado (`\'`).
Saca los pares clave-valor y quédate con los que llevan prosa: `q`, `a`, `t`, `title`, `label`,
`body`, `v`, `value`, `k`, `speaker`.

**3 · Recoge también el texto fijo del marcado**, el que no viene de plantilla: encabezados,
párrafos, notas al pie. Descarta todo lo que contenga `{{`.

**4 · Une las dos cosas.** Esa unión es el contenido de la página, y es lo que se compara contra la
fuente.

## Ubicar dónde cae cada diferencia

Dos anclas, y conviene usar ambas:

- **Comentarios de sección** en el marcado (`<!-- HERO -->`, `<!-- CIFRAS -->`, `<!-- ACCESO -->`,
  `<!-- FAQ -->`): delimitan bloques y suelen corresponder a los campos del esquema del sitio.
- **El nombre de la constante**: `faqs` ↔ el campo `faq`, `treatments` ↔ `treatments`, `videos` ↔
  `videos`. Cuando el nombre no calza con ningún campo (`impact`, `challenges`, `riskFactors`),
  **es contenido que la página tiene y el esquema no** — un hallazgo en dirección Design → fuente,
  no un error de lectura.

Una constante puede transformarse antes de renderizarse (`faqs` → `faqItems` vía `.map()`). El
contenido está en la constante de origen, no en la derivada.

## Reglas

- **No vuelques el HTML completo al contexto.** Una página real pesa decenas de miles de
  caracteres. Extrae el texto y trabaja con eso; si la lectura devuelve el archivo a disco, procesa
  desde ahí.
- **Si no encuentras el texto esperado, no concluyas que falta.** Primero comprueba si la sección
  usa plantilla y su constante existe. Ausente en el marcado ≠ ausente en la página.
- **Al reparar, edita la constante**, no el marcado renderizado — y respeta el escapado de comillas
  del original.
- **Si una página no usa plantillas** (las hay), el texto está en el marcado y basta el paso 3.

## Delegar

Cada página pesa decenas de miles de caracteres: verificar varias en el hilo principal consume el
contexto antes de llegar al reporte, y sin contexto no hay síntesis.

**Los subagentes acceden a los proyectos de diseño igual que la sesión principal** —comprobado:
`get_project`, `list_files` y `get_file` funcionan desde un subagente cuando el acceso de agentes
está concedido—. A partir de **tres piezas**, delega **una por subagente**, con su fila del mapeo y
las rutas de sus destinos.

Cada subagente devuelve **solo hallazgos estructurados** —pieza, destino, campo, texto de cada lado,
categoría—, **nunca el HTML ni el archivo completo**: si devuelve el contenido, no se ha ganado
nada. Si no pudo acceder a un destino, que lo diga; irá al reporte como no verificado, jamás como
coincidente.

**La síntesis no se delega**: reunir, aplicar el umbral de ruido y decidir qué merece la atención
del usuario se hace en el hilo principal.

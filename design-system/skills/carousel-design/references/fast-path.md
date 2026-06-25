# Anclaje del flujo — Rutas y ramificación post-chequeos

Este documento complementa el paso 0 del SKILL.md. El paso 0 define la secuencia rígida de tres chequeos (cliente, tipo de operación, sistema de diseño). Este archivo cubre las rutas en disco que se consultan después de cada chequeo y cómo se ramifica el flujo según las respuestas.

## 1. Convención de rutas

La raíz del repo es el directorio de trabajo. Los clientes viven directamente en ella.

```
[cliente]/
├── _recursos-cliente/
│   ├── sistema-de-diseno/              ← sistema de diseño del cliente
│   └── recursos/                       ← assets del cliente reutilizables entre carruseles
│       ├── iconos/
│       ├── logos/
│       ├── fondos/
│       └── imagenes/
└── carruseles/
    └── [carrusel]/
        ├── recursos/                   ← assets que aporta el usuario para esta pieza
        ├── publicar/                   ← PNGs retina exportados (entregable final)
        └── _skill-assets/              ← artefactos internos del skill
            ├── screenshots/            ← capturas de Chrome DevTools
            └── qa/                    ← reportes JSON y MD de control de calidad
```

## 2. Qué leer después de cada chequeo

El flujo no presupone nada. Lee disco únicamente cuando ya tiene la información que justifica esa lectura.

**Después del chequeo 0.1 (cliente confirmado):** todavía no leer nada. Esperar a tener también la respuesta de 0.2 antes de tocar disco.

**Después del chequeo 0.2 (tipo de operación confirmado):** ahora sí, ejecutar el chequeo 0.3 leyendo `{raiz}/[cliente]/_recursos-cliente/sistema-de-diseno/`. Esa es la única lectura del paso 0.

**Después del chequeo 0.3 (sistema de diseño verificado):**

- Si el sistema de diseño existe y la respuesta a 0.2 fue "nuevo": avanzar al paso 2, rama "nuevo".
- Si el sistema de diseño existe y la respuesta a 0.2 fue "retomamos": avanzar al paso 2, rama "retomamos" (listar `{raiz}/[cliente]/carruseles/` para identificar el carrusel a retomar).
- Si el sistema de diseño no existe: ir al paso 1 (construcción del paquete) sin importar la respuesta a 0.2. Cuando el paso 1 termine, volver a la rama correspondiente del paso 2.

## 3. Lógica de retoma

Cuando la respuesta a 0.2 fue "retomamos" y ya identificaste el carrusel específico, lee el estado del directorio `{raiz}/[cliente]/carruseles/[carrusel]/` para inferir en qué paso quedó la sesión previa. Señales útiles:

| Estado encontrado | Punto del flujo donde retomar |
|---|---|
| Directorio vacío o solo con `recursos/`, `publicar/`, `_skill-assets/` vacíos | Paso 3 (inventario de assets) |
| `recursos/` con imágenes pero sin `_skill-assets/color-palette.json` | Paso 6 (selección de colores) |
| `_skill-assets/color-palette.json` existe pero no hay `.html` | Paso 8 (propuesta para aprobación) o paso 9 (producción) |
| `.html` existe pero `_skill-assets/qa/` está vacío | Paso 11 (prueba visual) |
| `_skill-assets/qa/` tiene reportes y `.html` validado, sin PNGs en `publicar/` | Paso 12 (exportación PNG retina) |
| `_skill-assets/qa/`, `.html` y PNGs en `publicar/` presentes | Carrusel ya cerrado; preguntar al usuario qué quiere ajustar |

Estos son indicios, no certezas. Si el estado encontrado es ambiguo, informar al usuario en una frase breve qué se encontró y preguntar dónde quiere retomar — una sola pregunta, con opciones si ayuda a clarificar.

## 4. Lo que este flujo deliberadamente NO hace

No hay "fast path" basado en inferencia: aunque el cliente esté mencionado en el mensaje inicial, la skill pregunta 0.1 igual. Aunque el contexto del vault sugiera un cliente, la skill pregunta 0.1 igual. Aunque el sistema de diseño exista, la skill no avanza al paso 2 hasta que 0.1 y 0.2 fueron respondidas explícitamente.

La razón: la regularidad del flujo es lo que hace que el usuario confíe en él. Si a veces pregunta y a veces infiere, la skill se vuelve impredecible y termina haciendo preguntas vagas cuando la inferencia falla.

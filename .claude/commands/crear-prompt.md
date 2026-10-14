---
description: Genera el prompt autocontenido de Deep Research para la siguiente fase, una fase concreta o una iteración adicional
argument-hint: [investigacion] [fase opcional] [clase opcional: inicial|ampliacion|repeticion|verificacion] [foco opcional]
---

Genera un prompt **único y autocontenido** para que ChatGPT Deep Research ejecute una iteración de una fase sin ningún otro contexto (sin proyecto, sin instrucciones, sin conversaciones previas). Sigue `_sistema/protocolo.md` y `_sistema/convenciones.md`.

Argumentos: "$1" investigación (slug en `investigaciones/`; si hay una sola, úsala; si hay varias y no se indica, pregunta). "$2" fase (`F03`) — opcional. "$3" clase de iteración — opcional. El resto ("$ARGUMENTS" tras los anteriores) es un foco libre para ampliaciones ("solo reseñas de Tier 1").

## 1. Decidir qué prompt toca

- **Sin fase:** la `fase_actual`/`proximo_paso` de `00_proyecto/02-estado.md`; si no está claro, la primera fase en orden cuyo estado sea `reabierta`, `preparada` o `pendiente` y cuyas dependencias (`depende_de`) estén `consolidada`. Si las dependencias no están consolidadas, dilo y propón qué hacer antes en vez de generar el prompt.
- **Con fase:** esa fase. La iteración nueva es la siguiente a la última existente en su carpeta (`FXX-iNN-*`). Si ya existe un prompt en `borrador` sin informe para esa fase, avisa y pregunta si regenerarlo (sobrescribe ese mismo archivo) o crear otra iteración.
- **Clase** si no se indica: `inicial` si la fase no tiene informes; `repeticion` si la última revisión es `rechazado`; `ampliacion` si es `aceptado-parcial` (el prompt se limita a los huecos de esa revisión y de su sección "Qué falta"); `verificacion` solo si se pide.
- Si la ficha está en `pendiente` y es un borrador ("Borrador inicial" en el texto), **concreta antes la ficha** con lo aprendido en las fases consolidadas: objeto sin lectura genérica, preguntas revisadas, hipótesis (IDs reales), alcance, método, criterios de salida. Cambia su estado a `preparada`.
- Si la ficha dice `ejecutor: claude-code` o `promotor`, no generes un prompt para ChatGPT: explica qué habría que hacer y quién.

## 2. Reunir el contexto (lee, no resumas de memoria)

Lee enteros: `00_proyecto/01-contexto.md`, `02-estado.md`, `05-conclusiones.md`, `04-hipotesis.md`, `06-decisiones.md`, `07-preguntas.md`, `03-datos-clave.md`, la `ficha.md` de la fase, las `sintesis.md` de las fases de las que depende y, si es una iteración posterior, las revisiones anteriores de esa fase.

Selecciona **solo lo relevante para esta fase** (un prompt largo pero sin ruido; orientativo 1.500– 3.500 palabras):

- Conclusiones: las `solida`/`provisional` que afecten a la fase, con su confianza. Nunca las `invalidada`.
- Datos: los de `03-datos-clave.md` que el investigador necesita para no reinvestigar (tablas compactas). Los marcados ⚠ van como "por verificar", no como hechos.
- Decisiones: las `adoptada` como restricciones; las `propuesta` como "recomendación vigente, puedes cuestionarla con evidencia".
- "No asumir": hipótesis refutadas, afirmaciones rechazadas en revisiones anteriores y lo que `05-conclusiones.md` dice que no se sabe.
- Hipótesis: las de la ficha, con su estado y evidencia actual en una línea.
- Preguntas con `responde: promotor` que sigan abiertas: **no** se le piden al investigador; si afectan a la fase, menciónalo en "Limitaciones conocidas" dentro de la sección C. Si el promotor ya ha aportado el dato (en el registro o en la conversación), inclúyelo como hecho.

## 3. Redactar el prompt

Copia `_sistema/plantillas/prompt.md` a `investigaciones/$1/fases/<carpeta-fase>/FXX-iNN-prompt.md` y sustituye todos los `{{...}}`:

- Todo en español, en segunda persona, sin referencias que el investigador no pueda resolver ("como vimos en la Fase 2", "el informe anterior", rutas de archivos, IDs sin explicar). Los IDs (`H-05`) se pueden usar siempre que vayan con su enunciado: sirven para que el informe los cite de vuelta.
- `{{objeto}}`: el de la ficha, concreto (negocio, servicio, lugar, capacidad).
- `{{contexto}}`: condensado de `01-contexto.md` con lo que importa para la fase (precios, capacidad, restricciones del promotor, activos). Hechos, no opiniones.
- `{{preguntas}}`: numeradas `Q1…Qn`, de la ficha, ajustadas a la clase de iteración.
- `{{bloque_iteracion}}`: vacío en `inicial`. En `repeticion`/`ampliacion`/`verificacion`, una sección `## Por qué hay una nueva iteración` con los errores concretos de las iteraciones previas que no deben repetirse (de las revisiones) o los huecos exactos a cubrir. Sin mencionar archivos.
- `{{metodo}}`: fuentes y procedimiento específicos de la fase (de la ficha), con mínimos de exhaustividad cuando aplique (p. ej. tamaño de muestra, nº de competidores).
- En la estructura de entrega, ajusta "Q1…Qn" al número real de preguntas.
- Frontmatter: `estado: borrador`, `clase`, `iteracion`, fecha de hoy. Bajo el título, una nota con qué registros se usaron para generarlo.

## 4. Comprobar antes de entregar

- Busca `{{` en el archivo: no debe quedar ninguno.
- Relee el bloque como si fueras ChatGPT sin contexto: ¿se entiende qué negocio, qué ciudad, qué servicio y qué se pide sin nada más? ¿Hay alguna instrucción que contradiga `06-decisiones.md`?
- Actualiza la tabla "Iteraciones" de la ficha (fila nueva con el enlace al prompt), su estado (`preparada`) y, en `02-estado.md`, `fase_actual`, `proximo_paso`, la fila de la fase y una línea de bitácora.
- Ejecuta `python3 _sistema/scripts/validar.py $1` y corrige los errores.

## 5. Entregar

Dile al usuario la ruta del prompt, en 3–5 líneas qué pide y por qué (qué huecos cubre), su extensión aproximada, y los pasos: abrir en Obsidian → copiar el bloque → conversación nueva de ChatGPT con Deep Research → descargar el informe en `.md` → `/ingerir-informe $1 FXX` (lo busca en `~/Downloads`). Cuando el usuario confirme que lo ha enviado, cambia el prompt a `estado: enviado`.

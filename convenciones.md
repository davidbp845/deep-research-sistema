---
tipo: protocolo
fecha_actualizacion: 2026-10-08
tags: [sistema, convenciones]
---

# Convenciones de archivos

`_sistema/scripts/validar.py` comprueba todo lo que aquí es obligatorio. Si una regla cambia, cambia también el validador.

## Estructura

```text
<proyecto>/                        ← vault de Obsidian + repo git (contenedor, con tus investigaciones)
├── CLAUDE.md                      ← importa _sistema/CLAUDE.md y añade lo específico del proyecto
├── .claude/commands/              ← symlinks a _sistema/.claude/commands/
├── _sistema/                      ← submódulo deep-research-sistema: motor genérico (sin datos de ninguna investigación)
│   ├── protocolo.md               ← metodología y criterios de revisión
│   ├── convenciones.md            ← este archivo
│   ├── plantillas/                ← plantillas que copian las órdenes (y las del contenedor en proyecto/)
│   └── scripts/                   ← validar.py (validador + tablero), normalizar.py, crear-proyecto.sh
└── investigaciones/<slug>/        ← una carpeta por investigación
    ├── 00_proyecto/
    │   ├── 01-contexto.md         ← objeto, negocio, restricciones (fuente de la sección "Contexto" de cada prompt)
    │   ├── 02-estado.md           ← tablero de fases, conocimiento actual, próximo paso, bitácora
    │   ├── 03-datos-clave.md      ← hechos verificados reutilizables (tablas con fuente y fecha)
    │   ├── 04-hipotesis.md        ← registro H-xx
    │   ├── 05-conclusiones.md     ← registro C-xx
    │   ├── 06-decisiones.md       ← registro D-xx
    │   └── 07-preguntas.md        ← registro P-xx
    ├── fases/FXX-<slug-fase>/
    │   ├── ficha.md               ← definición de la fase
    │   ├── FXX-iNN-prompt.md      ← prompt enviado al investigador
    │   ├── FXX-iNN-informe.md     ← informe recibido (normalizado, cuerpo sin reescribir)
    │   ├── FXX-iNN-revision.md    ← auditoría de Claude Code y veredicto
    │   └── sintesis.md            ← lo consolidado de la fase (se reescribe al consolidar)
    └── _archivo/                  ← material histórico que no forma parte del ciclo
```

Nombres en minúsculas, sin espacios ni tildes. Fases `F01`…`F99`, iteraciones `i01`…`i99`.

## Enlaces

Se usan **enlaces Markdown relativos** (`[F02-i02](../fases/F02-mercado-competencia/F02-i02-informe.md)`), no wikilinks: en un vault con varias investigaciones los nombres `02-estado.md` o `ficha.md` se repiten y un wikilink sería ambiguo. Obsidian los sigue y los muestra en el grafo igual.

## Identificadores

| Prefijo | Registro | Ejemplo |
|---|---|---|
| `C-` | conclusiones | `C-03` |
| `H-` | hipótesis | `H-05` |
| `D-` | decisiones | `D-02` |
| `P-` | preguntas pendientes | `P-07` |
| `E-` | datos clave (evidencia verificada) | `E-12` |

Son únicos dentro de una investigación, correlativos y **nunca se reutilizan ni se borran**: cuando algo deja de valer, cambia de `estado`. Cualquier documento puede citarlos (`H-05`); el validador avisa si un ID citado no existe en su registro.

## Formato de un elemento de registro

Cada elemento es un encabezado `###` seguido de una lista de campos. Los campos obligatorios están en negrita en la tabla de cada registro.

```markdown
### H-05 — El dolor/tensión de cuello y espalda es el principal motivo de reserva

- estado: abierta
- confianza: media
- origen: F02-i02
- fases: F03
- evidencia: …
- validar_con: …
- historial:
  - 2026-10-08 — creada a partir de F02-i02 §10.
```

| Registro | Campos | Valores de `estado` |
|---|---|---|
| conclusiones | **estado**, **confianza**, **origen**, evidencia, implicacion, historial | `solida`, `provisional`, `debilitada`, `invalidada` |
| hipotesis | **estado**, **confianza**, **origen**, fases, evidencia, validar_con, historial | `abierta`, `apoyada`, `refutada`, `descartada`, `validada` |
| decisiones | **estado**, **origen**, motivo, revisar_si, historial | `propuesta`, `adoptada`, `revocada` |
| preguntas | **estado**, **prioridad**, **responde**, fase, historial | `abierta`, `respondida`, `descartada` |

- `confianza`: `alta`, `media-alta`, `media`, `baja`.
- `origen`: iteración (`F02-i02`), `promotor` o `claude-code`.
- `responde` (preguntas): `investigacion` (se puede buscar fuera), `promotor` (dato interno) o `experimento` (solo se sabe midiendo).
- `validada` (hipótesis) se reserva para lo confirmado con **datos reales del negocio**; lo que solo apoya la investigación de escritorio queda en `apoyada`.
- Una decisión `propuesta` es una recomendación de la investigación; solo el promotor la pasa a `adoptada`.

## Frontmatter por tipo de documento

Campos comunes a todo documento de una investigación: `tipo`, `investigacion` (slug), `fecha_actualizacion` (AAAA-MM-DD).

| `tipo` | Campos propios obligatorios | Valores |
|---|---|---|
| `contexto` | — | |
| `estado` | `fase_actual`, `proximo_paso` | |
| `registro` | `registro` | `conclusiones`, `hipotesis`, `decisiones`, `preguntas`, `datos` |
| `fase` | `fase`, `titulo`, `estado`, `ejecutor`, `depende_de`, `iteracion_aceptada` | estado: `pendiente`, `preparada`, `en-investigacion`, `en-revision`, `consolidada`, `reabierta`, `descartada` |
| `prompt` | `fase`, `iteracion`, `clase`, `estado`, `destino` | clase: `inicial`, `ampliacion`, `repeticion`, `verificacion`; estado: `borrador`, `enviado`, `respondido`, `descartado` |
| `informe` | `fase`, `iteracion`, `origen`, `fecha_recepcion`, `veredicto` | veredicto: `pendiente`, `aceptado`, `aceptado-parcial`, `rechazado` |
| `revision` | `fase`, `iteracion`, `veredicto`, `puntuacion` | puntuacion: entero 0–20 |
| `sintesis` | `fase`, `iteraciones_consolidadas`, `confianza_global` | |

`iteracion_aceptada` y `prompt`/`informe` en blanco se escriben como `null`.

## Normalización de informes

El cuerpo de un informe **no se reescribe**: es la evidencia de qué entregó el investigador. Al ingerirlo solo se:

- añade/sustituye el frontmatter;
- eliminan artefactos de la interfaz de ChatGPT (marcadores de cita `cite…`/`turn…`, caracteres de uso privado `U+E000–U+F8FF`, `【…】`);
- sustituyen envoltorios HTML (`<div>`, `<figure>`, `<br>`…) por su contenido Markdown.

Cualquier corrección de contenido va a la revisión o a los registros, nunca al informe.

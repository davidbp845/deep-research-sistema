# deep-research-sistema

Motor reutilizable para llevar **investigaciones profundas por fases** con memoria persistente en Markdown: Claude Code mantiene el protocolo y la memoria, genera prompts autocontenidos y audita lo que vuelve; un investigador externo (por defecto ChatGPT Deep Research) investiga; tú decides.

Nació porque los informes de los investigadores automáticos están muy bien escritos y tienen errores que nadie detecta: cifras sin fuente, cálculos que no cuadran, competidores inventados o conclusiones que no se siguen de los datos. Aquí cada informe se revisa con criterios fijos, se le pone nota y solo lo que se sostiene pasa a la memoria del proyecto.

Este repo no contiene ninguna investigación: se usa como submódulo dentro de un **proyecto de investigaciones** (un repo tuyo, normalmente privado), igual que un motor se monta en un coche.

## Cómo funciona

| Paso | Quién | Qué |
|---|---|---|
| 1 | Claude Code | `/crear-prompt <investigacion> [fase] [clase]` prepara un prompt único con todo el contexto: objeto, negocio, lo que ya se sabe, hipótesis a refutar, preguntas, método y formato de entrega. |
| 2 | Tú | Abres el prompt en Obsidian, copias el bloque y lo pegas en una conversación **nueva** de ChatGPT con Deep Research (sin proyecto ni instrucciones). |
| 3 | Tú | Descargas el informe en `.md` (queda en `~/Downloads`). |
| 4 | Claude Code | `/ingerir-informe <investigacion> <fase> [ruta]` lo limpia, lo guarda en su fase y lo audita: nota 0–20 y veredicto (`aceptado`, `aceptado-parcial`, `rechazado`). |
| 5 | Tú + Claude Code | Si se acepta, `/consolidar-fase` pasa lo válido a los registros. Si no, `/crear-prompt` con otra iteración centrada en lo que falló. |
| 6 | Tú | Revisas las decisiones en `propuesta` y marcas como `adoptada` lo que aceptes. Aportas los datos que solo tú tienes (preguntas con `responde: promotor`). |

`/estado` muestra el avance en cualquier momento y `/ayuda` lista los comandos. La metodología completa (fases, iteraciones, criterios de revisión R1–R10, consolidación) está en [`protocolo.md`](protocolo.md) y el formato de cada archivo en [`convenciones.md`](convenciones.md).

## Qué guarda cada investigación

```text
investigaciones/<slug>/
├── 00_proyecto/          numerados por orden de lectura
│   ├── 01-contexto.md       objeto, negocio, restricciones (lo único que no se investiga)
│   ├── 02-estado.md         tablero de fases, qué sabemos, próximo paso, bitácora
│   ├── 03-datos-clave.md    E-xx: hechos verificados con fuente y fecha
│   ├── 04-hipotesis.md      H-xx: lo que se intenta refutar
│   ├── 05-conclusiones.md   C-xx: lo que se sostiene, con su confianza
│   ├── 06-decisiones.md     D-xx: propuestas por la investigación, adoptadas por ti
│   └── 07-preguntas.md      P-xx: lo pendiente y quién puede responderlo
├── fases/FXX-<slug>/     ficha, y por iteración: prompt, informe y revisión; síntesis al consolidar
└── _archivo/             material histórico (no se valida ni se edita)
```

Los elementos de los registros nunca se borran ni se renumeran: cambian de estado y acumulan un `historial` con la evidencia de cada cambio.

## Crear tu proyecto de investigaciones

### Requisitos

- [Claude Code](https://claude.com/claude-code).
- Python 3 con PyYAML (`pip install pyyaml`) para el validador.
- Un investigador externo: el sistema está pensado para ChatGPT Deep Research, pero el prompt es texto autocontenido y vale para cualquier otro.
- [Obsidian](https://obsidian.md) (opcional): el proyecto es un vault y se lee mucho mejor ahí.

### Con el script

```bash
git clone https://github.com/davidbp845/deep-research-sistema.git /tmp/deep-research-sistema
/tmp/deep-research-sistema/scripts/crear-proyecto.sh ~/mis-investigaciones
cd ~/mis-investigaciones
claude
```

Y dentro de Claude Code:

```text
/nueva-investigacion <slug>
```

`/nueva-investigacion` te entrevista solo para lo que no se puede investigar (objeto, qué existe hoy, restricciones, tus hipótesis de partida), crea los registros y propone el plan de fases. Después, `/crear-prompt <slug>` genera el primer prompt.

El script crea un repo git en la carpeta indicada, añade este motor como submódulo en `_sistema/`, enlaza los comandos, copia el `CLAUDE.md`, el `README.md`, el `.gitignore` y la configuración de Obsidian desde [`plantillas/proyecto/`](plantillas/proyecto/) y [`obsidian/`](obsidian/), y hace el primer commit. No crea remoto ni sube nada: tus investigaciones son tuyas. Si quieres usar tu propio fork del motor, pásale su URL como segundo argumento.

### A mano

Lo mismo que hace el script, por si prefieres verlo paso a paso:

```bash
mkdir mis-investigaciones && cd mis-investigaciones && git init
git submodule add https://github.com/davidbp845/deep-research-sistema.git _sistema
mkdir -p investigaciones .claude/commands .obsidian/snippets
for c in _sistema/.claude/commands/*.md; do ln -s "../../$c" .claude/commands/; done
cp _sistema/plantillas/proyecto/CLAUDE.md CLAUDE.md          # sustituye {{proyecto}}
cp _sistema/plantillas/proyecto/README.md README.md          # sustituye {{proyecto}}
cp _sistema/plantillas/proyecto/gitignore .gitignore
cp _sistema/obsidian/*.json .obsidian/ && cp _sistema/obsidian/snippets/*.css .obsidian/snippets/
```

El `CLAUDE.md` del proyecto importa las reglas del motor (`@_sistema/CLAUDE.md`) y deja sitio para lo tuyo: qué otros repos o documentos pueden leer las investigaciones y qué manda si se contradicen.

### Estructura resultante

```text
mis-investigaciones/          ← tu repo (privado) y vault de Obsidian
├── CLAUDE.md                 ← @_sistema/CLAUDE.md + lo específico de tu proyecto
├── README.md                 ← índice de tus investigaciones
├── .claude/commands/         ← symlinks a _sistema/.claude/commands/
├── .obsidian/                ← configuración de partida (ancho de lectura a 65 caracteres)
├── investigaciones/<slug>/   ← cada investigación
└── _sistema/                 ← este repo, como submódulo
```

## Mantenimiento

```bash
python3 _sistema/scripts/validar.py [slug] [--estado]   # comprueba frontmatter, IDs, estados y enlaces; --estado añade el tablero
python3 _sistema/scripts/normalizar.py entrada.md salida.md   # limpia un informe pegado de ChatGPT sin tocar su contenido
git submodule update --remote _sistema                  # trae la última versión del motor (después: git add _sistema)
```

Si el motor añade un comando nuevo, crea su symlink en `.claude/commands/` (o vuelve a ejecutar el bucle `for` de arriba).

## Contribuir

Este repo es genérico: nada de un negocio, persona o investigación concretos. Si cambias una regla de [`convenciones.md`](convenciones.md), cambia también `scripts/validar.py`, las plantillas y los comandos afectados. Las reglas para Claude Code están en [`CLAUDE.md`](CLAUDE.md).

# deep-research-sistema — reglas para Claude Code

Este archivo lo importa el `CLAUDE.md` de cada proyecto de investigaciones (`@_sistema/CLAUDE.md`). Las rutas son relativas a la raíz de ese proyecto, donde este repo está montado como submódulo en `_sistema/`.

Sistema para gestionar investigaciones profundas por fases: Claude Code mantiene la memoria y el protocolo, genera prompts autocontenidos y audita lo que vuelve; un investigador externo (por defecto ChatGPT Deep Research) investiga; el promotor decide. El proyecto se abre como vault de Obsidian desde su raíz.

La metodología está en [`_sistema/protocolo.md`](protocolo.md) y el formato de archivos, frontmatter, IDs y estados en [`_sistema/convenciones.md`](convenciones.md). Léelos antes de tocar una investigación; no se repiten aquí.

## Reglas al trabajar en un proyecto

- **La memoria vive en los archivos.** Antes de opinar sobre una investigación, lee su `00_proyecto/` (contexto, estado y registros). No resumas de memoria lo que dice un informe: ábrelo.
- **Los informes no se reescriben.** El cuerpo de `FXX-iNN-informe.md` es evidencia de lo que entregó el investigador; solo se normaliza (`_sistema/scripts/normalizar.py`). Las correcciones van a la revisión o a los registros.
- **Solo `/consolidar-fase` escribe en los registros a partir de un informe.** Los elementos nunca se borran ni se renumeran: cambian de estado y se añade una línea de `historial` con la evidencia.
- **Las decisiones `adoptada` son del promotor.** La investigación solo crea o cambia decisiones en `propuesta`.
- **Crítico, no complaciente.** La razón de existir de este sistema es que los informes de los investigadores automáticos tienen errores que nadie detecta. Revisa con los criterios R1–R10 del protocolo, rehaz los cálculos y señala lo que no se sostiene, aunque el informe esté bien escrito.
- **Prompts autocontenidos.** Un prompt nunca depende de conversaciones, archivos o proyectos del investigador: todo lo necesario va dentro (`_sistema/plantillas/prompt.md`).
- **Sin cortes de línea manuales en los `.md`.** Cada párrafo, punto de lista o pregunta va en una sola línea; el ancho de lectura lo pone el CSS de Obsidian (`.obsidian/snippets/ancho-lectura.css`).
- **Ejecuta `python3 _sistema/scripts/validar.py` antes de dar algo por terminado.** Con `--estado` muestra además el tablero de avance.
- `_archivo/` de cada investigación guarda material histórico (conversaciones con el investigador, versiones descartadas): no se valida ni se edita.

## El motor y el proyecto son repos distintos

- **`_sistema/` es genérico y público:** sin referencias a ningún negocio, persona o investigación concreta. Lo específico va en `investigaciones/<slug>/00_proyecto/01-contexto.md` o en el `CLAUDE.md` del proyecto.
- Desde un proyecto, `_sistema/` no se toca salvo para actualizar el motor (`git submodule update --remote _sistema`) o para mejorarlo entrando en esa carpeta como el repo aparte que es (commit y push desde `_sistema/`, y después `git add _sistema` en el proyecto para mover el puntero).
- Si cambias una regla de `convenciones.md`, cambia también `scripts/validar.py`, las plantillas y los comandos afectados, y comprueba que el validador sigue pasando en algún proyecto real.
- Los comandos viven en `_sistema/.claude/commands/`; el proyecto los enlaza con symlinks desde su `.claude/commands/`. Un comando nuevo necesita su symlink en cada proyecto (`scripts/crear-proyecto.sh` los crea todos).

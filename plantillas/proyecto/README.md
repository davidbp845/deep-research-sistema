# {{proyecto}}

Investigaciones profundas por fases, con memoria persistente en Markdown. Ábrelo en Obsidian desde esta carpeta.

El motor (protocolo, convenciones, plantillas, scripts y comandos de Claude Code) es el submódulo [`_sistema/`](_sistema/README.md): el flujo de trabajo y las reglas están explicados allí una sola vez.

## Investigaciones

<!-- /nueva-investigacion añade aquí cada investigación: - [slug](investigaciones/<slug>/00_proyecto/02-estado.md) — descripción. -->

## Uso rápido

- `/nueva-investigacion <slug>` — da de alta una investigación.
- `/crear-prompt` → investigador → `/ingerir-informe` → `/consolidar-fase` → `/estado`.
- `/ayuda` lista todos los comandos.
- `python3 _sistema/scripts/validar.py --estado` comprueba todo y muestra el tablero.
- `git submodule update --remote _sistema` actualiza el motor.

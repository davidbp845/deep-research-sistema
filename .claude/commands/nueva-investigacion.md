---
description: Crea una investigación nueva a partir del esqueleto (contexto, registros y fases)
argument-hint: [slug]
---

Da de alta una investigación en `investigaciones/$1/` (slug en minúsculas, con guiones, p. ej. `mercado-app-reservas`). Si ya existe, avisa y no sobrescribas nada.

1. Crea `investigaciones/$1/00_proyecto/` copiando de `_sistema/plantillas/`: `01-contexto.md`, `02-estado.md`, `05-conclusiones.md`, `04-hipotesis.md`, `06-decisiones.md`, `07-preguntas.md`, `03-datos-clave.md`. Sustituye `{{investigacion}}`, `{{titulo_investigacion}}` y `{{fecha}}`. Crea también `fases/` y `_archivo/`.
2. **Entrevista breve al usuario para el contexto** (es lo único que no se puede investigar): objeto y pregunta de negocio, qué existe hoy (hechos), capacidades y restricciones (tiempo, presupuesto, canales vetados), principios propios y un primer plan de fases. Si el usuario señala fuentes internas (otro repo, un plan de empresa, un vault de notas), léelas y propón el contexto tú en vez de preguntar lo que ya está escrito. Pregunta solo lo que falte.
3. Registra las restricciones del promotor como decisiones `adoptada` con `origen: promotor`, y las hipótesis de partida del promotor en `04-hipotesis.md` (para que la investigación intente refutarlas).
4. Crea las fichas del plan de fases (puedes usar `/nueva-fase` para cada una): la primera concretada y `preparada`; las demás como borrador inicial.
5. Rellena `02-estado.md`, añade la investigación a la sección «Investigaciones» del `README.md` del proyecto (`- [$1](investigaciones/$1/00_proyecto/02-estado.md) — descripción en una línea.`) y ejecuta `python3 _sistema/scripts/validar.py $1 --estado`.
6. Ofrece generar el primer prompt con `/crear-prompt $1`.

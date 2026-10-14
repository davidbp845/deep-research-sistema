---
description: Pasa lo aceptado de una iteración revisada a la memoria del proyecto (registros, síntesis y estado)
argument-hint: [investigacion] [fase] [iteracion opcional]
---

Incorpora a la memoria del proyecto lo que la revisión de una iteración marca como consolidable. Es el único paso que modifica `05-conclusiones.md`, `04-hipotesis.md`, `06-decisiones.md`, `07-preguntas.md` y `03-datos-clave.md` a partir de un informe.

Argumentos: "$1" investigación, "$2" fase, "$3" iteración (por defecto, la última con revisión `aceptado` o `aceptado-parcial` no consolidada todavía — ver `iteraciones_consolidadas` de la síntesis). Si el veredicto es `rechazado`, no consolides: como mucho registra las hipótesis y preguntas que la revisión marque explícitamente como útiles, y dilo.

## Pasos

1. Lee la revisión, el informe, la ficha, la síntesis actual (si existe) y todos los registros.
2. Aplica la sección "Qué se puede consolidar" de la revisión, verificando cada punto contra el informe (no copies de la revisión sin mirar la evidencia):
   - **Nuevos elementos:** siguiente ID libre, formato de `_sistema/convenciones.md`, `origen: FXX-iNN`, confianza ajustada a la evidencia real (no a la que declara el informe), y una línea de `historial`.
   - **Elementos existentes que cambian:** nunca se borran ni se reescribe su historia. Cambia `estado`/`confianza`, actualiza `evidencia` si procede y añade una línea al `historial` con fecha, iteración y **qué evidencia provoca el cambio**. Si una conclusión queda `invalidada`, revisa qué decisiones (`motivo`) e hipótesis dependían de ella y márcalo también.
   - **Hipótesis:** `apoyada`/`refutada` según el informe; `validada` solo con datos reales del negocio.
   - **Decisiones:** la investigación solo crea o modifica decisiones en estado `propuesta`. Una `adoptada` solo cambia si el usuario lo pide; si la evidencia la cuestiona, abre una pregunta y avísale.
   - **Preguntas:** marca `respondida` las que el informe responda (enlazando el elemento que las responde); añade las nuevas.
   - **Datos:** solo hechos con fuente y fecha; los dudosos con ⚠ o como pregunta.
3. Reescribe `sintesis.md` de la fase (plantilla `_sistema/plantillas/sintesis.md`): respuesta a la pregunta principal, qué sabemos, qué no, qué cambió, IDs afectados; añade la iteración a `iteraciones_consolidadas`.
4. Ficha: `iteracion_aceptada`, `estado: consolidada` (o `reabierta` si la revisión pide otra iteración imprescindible para los criterios de salida).
5. `02-estado.md`: tabla de fases, secciones de conocimiento (sólido / provisional / desconocido), próximo paso razonado (qué fase o iteración sigue y por qué; qué datos del promotor ayudarían) y bitácora.
6. Revisa si lo consolidado afecta a fichas de fases **pendientes** (preguntas que sobran o faltan, hipótesis nuevas) y ajústalas.
7. `python3 _sistema/scripts/validar.py $1 --estado`; corrige errores.
8. Propón un commit (`git add -A && git commit`) con un mensaje que diga qué fase/iteración se ha consolidado y los cambios más importantes; hazlo si el usuario no ha dicho lo contrario.

Resume al usuario: qué entra en la memoria, qué conclusiones anteriores cambian y por qué, decisiones `propuesta` nuevas que le toca aceptar o rechazar, y el próximo paso.

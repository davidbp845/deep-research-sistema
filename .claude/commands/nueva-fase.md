---
description: Añade una fase nueva (o reordena el plan) en una investigación
argument-hint: [investigacion] [titulo de la fase] [posición opcional, p. ej. "antes de F05"]
---

Las fases son orientativas y cambian con lo que se aprende. Esta orden añade una.

1. Lee `01-contexto.md`, `02-estado.md` y las fichas existentes de "$1".
2. Asigna el siguiente número libre (`F09`…). Los números **no se reordenan ni se reutilizan**: si la fase debe ir antes que otras, se expresa con `depende_de` de las fichas afectadas y con el orden de la tabla de `02-estado.md`, no renumerando carpetas (rompería enlaces y referencias).
3. Crea `investigaciones/$1/fases/FXX-<slug>/ficha.md` desde `_sistema/plantillas/ficha.md` y rellénala a partir de lo que pida el usuario y de lo consolidado: objeto concreto, pregunta principal, para qué sirve, preguntas, hipótesis (IDs existentes o nuevas en `04-hipotesis.md`), alcance, método, criterios de salida, `ejecutor` y `depende_de`. Si es muy pronto para concretarla, márcala como borrador inicial.
4. Si la fase nueva sustituye o absorbe otra, pon la otra en `estado: descartada` con una nota (no la borres) y ajusta las preguntas de `07-preguntas.md` cuya `fase` cambie.
5. Actualiza la tabla y la bitácora de `02-estado.md` y el plan de fases de `01-contexto.md`.
6. `python3 _sistema/scripts/validar.py $1`.

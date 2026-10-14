---
description: Muestra el avance de una investigación, lo que sabemos, lo pendiente y el próximo paso
argument-hint: [investigacion opcional]
---

Resume el estado de "$1" (o de todas las investigaciones si no se indica). Solo lectura: no modifiques nada salvo que el validador encuentre incoherencias que el usuario te pida corregir.

1. Ejecuta `python3 _sistema/scripts/validar.py $1 --estado` y muestra su tablero.
2. Lee `investigaciones/$1/00_proyecto/02-estado.md` y los registros, y añade en pocas líneas:
   - conclusiones más importantes (sólidas y provisionales, con su confianza);
   - decisiones en `propuesta` esperando al promotor;
   - preguntas abiertas con `responde: promotor` (lo que solo él puede aportar);
   - prompts en `borrador`/`enviado` sin informe;
   - próximo paso recomendado y por qué.
3. Si el validador da errores o avisos, enuméralos y propone cómo arreglarlos.

---
description: Incorpora un informe de ChatGPT a su fase, lo normaliza y lo audita con veredicto
argument-hint: [investigacion] [fase] [ruta del .md descargado (opcional)]
---

Recibe el resultado de una iteración, lo guarda limpio y lo **revisa críticamente** con los criterios de `_sistema/protocolo.md`. No consolida nada en los registros: eso es `/consolidar-fase`, después de que el usuario vea el veredicto.

Argumentos: "$1" investigación, "$2" fase (`F03`), "$3" ruta del `.md` descargado de ChatGPT. Si no se indica ruta, busca el `.md` más reciente de `~/Downloads` (`ls -t ~/Downloads/*.md | head`), enséñale al usuario el nombre, la fecha y las primeras líneas, y confirma que es el informe antes de seguir. Si el usuario lo pega en el mensaje en vez de descargarlo, guárdalo tú primero en el scratchpad. El archivo original de Descargas no se mueve ni se borra. Si falta la fase, dedúcela del prompt en estado `enviado`/`borrador` más reciente y confírmalo.

## 1. Guardar y normalizar

1. Determina la iteración: la del prompt pendiente de esa fase (el último `FXX-iNN-prompt.md` sin informe). Si no hay prompt (informe hecho fuera del sistema), usa la siguiente iteración libre y `prompt: null`.
2. `python3 _sistema/scripts/normalizar.py <entrada> investigaciones/$1/fases/<carpeta>/FXX-iNN-informe.md` e informa de lo que ha limpiado.
3. Sustituye o añade el frontmatter (`tipo: informe`, `fase`, `iteracion`, `origen` — p. ej. `chatgpt-deep-research` —, `prompt: FXX-iNN-prompt.md` o `null`, `fecha_recepcion`, `veredicto: pendiente`, `fecha_actualizacion`). **No reescribas el cuerpo**: es la evidencia de lo que entregó el investigador. Si trae Mermaid, déjalo y anótalo en la revisión.
4. Si el texto parece truncado (sección de fuentes ausente, final abrupto) o es un resumen en vez del informe, avisa antes de seguir: puede ser una exportación incompleta.
5. Marca el prompt como `estado: respondido`.

## 2. Revisar (la parte importante)

Lee el informe **entero**, el prompt de esa iteración, la ficha, `01-contexto.md` y los registros. Crea `FXX-iNN-revision.md` desde `_sistema/plantillas/revision.md` y rellénalo:

- **Puntuación R1–R10** (0/1/2) con un motivo concreto por criterio y el veredicto según las reglas del protocolo.
- **Cobertura pregunta a pregunta** contra las `Q` del prompt.
- **Errores y afirmaciones no sostenidas:** cifras sin fuente, estimaciones presentadas como hechos, cálculos que no cuadran (rehaz las cuentas), fuentes citadas sin URL, URLs genéricas, datos inconsistentes entre secciones, recomendaciones que violan restricciones de `01-contexto.md` o decisiones `adoptada`.
- **Contradicciones con lo consolidado:** compara con `05-conclusiones.md` y `03-datos-clave.md`. Para cada una, cuál se sostiene mejor y por qué (calidad, actualidad, metodología, proximidad).
- **Verificación puntual (si hay acceso web):** comprueba 3–5 datos críticos del informe (los que más peso tienen en sus conclusiones) con WebFetch/WebSearch y anota el resultado. No investigues más allá: el objetivo es medir la fiabilidad, no rehacer la fase.
- **Qué se puede consolidar:** lista de candidatos con el ID nuevo que tendrían (siguiente libre) o el ID existente que modifican, y con qué estado/confianza.
- **Qué falta / siguiente iteración recomendada:** si procede otra iteración, sus huecos concretos.

Sé exigente: un informe largo y bien formateado puede ser malo. El veredicto lo propone Claude Code; el usuario lo puede cambiar.

## 3. Actualizar y entregar

- Frontmatter del informe: `veredicto`. Ficha: fila de la tabla de iteraciones y `estado: en-revision`. `02-estado.md`: fila de la fase, `proximo_paso` y bitácora.
- `python3 _sistema/scripts/validar.py $1`.
- Resume al usuario: veredicto y nota, 3–5 hallazgos más valiosos, 3–5 problemas principales, qué cambiaría del conocimiento actual, y la recomendación: `/consolidar-fase $1 FXX` (si es aceptado o aceptado-parcial) y/o `/crear-prompt $1 FXX <clase>` para otra iteración.

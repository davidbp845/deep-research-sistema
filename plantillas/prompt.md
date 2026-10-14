---
tipo: prompt
investigacion: {{investigacion}}
fase: {{FXX}}
iteracion: {{iNN}}
clase: {{clase}}
estado: borrador
destino: chatgpt-deep-research
fecha_actualizacion: {{fecha}}
---

# Prompt {{FXX}}-{{iNN}} — {{titulo_fase}}

> Copia el bloque de abajo entero (botón de copiar del bloque en Obsidian) y pégalo en una conversación **nueva** de ChatGPT con Deep Research activado. No hace falta proyecto ni instrucciones: el prompt es autocontenido. Cuando termine, descarga el informe en `.md` y ejecuta `/ingerir-informe {{investigacion}} {{FXX}}` (busca el `.md` más reciente en `~/Downloads`; o pásale la ruta).

````text
INVESTIGACIÓN PROFUNDA — {{titulo_investigacion}}
Fase {{FXX}}: {{titulo_fase}} · Iteración {{iNN}} ({{clase}}) · {{fecha}}

## A. Cómo trabajar este encargo

- Este mensaje contiene TODO el contexto necesario. No existen conversaciones previas que debas recordar o buscar: lo que no esté aquí, no lo sabemos.
- No hagas preguntas de aclaración antes de empezar. Si algo es ambiguo, elige la interpretación más fiel al objeto de la sección B y decláralo en "Limitaciones".
- Investiga solo esta fase. No rehagas trabajo que la sección D da por resuelto, salvo que encuentres evidencia nueva que lo contradiga (en ese caso, dilo explícitamente).
- Dedica el esfuerzo a la profundidad y la verificación, no a la extensión. Prefiero 20 hechos bien verificados a 100 recopilados de forma superficial. "No lo sabemos" es un resultado válido.

## B. Objeto de la investigación

{{objeto}}

Control de deriva: si en algún momento el análisis pasa a tratar otra ciudad, otro producto, otro tipo de negocio o un "caso genérico", detente y vuelve a este objeto. Un informe genérico no sirve.

## C. Contexto del negocio

{{contexto}}

## D. Lo que ya sabemos (estado acumulado de la investigación)

### D.1 Conclusiones consolidadas
{{conclusiones}}

### D.2 Datos verificados reutilizables
{{datos}}

### D.3 Decisiones vigentes
{{decisiones}}

### D.4 Lo que NO está demostrado y no debes asumir
{{no_asumir}}

## E. Objetivo de esta fase

Pregunta principal: {{pregunta_principal}}

Para qué sirve la respuesta: {{para_que}}

Preguntas que debes responder:
{{preguntas}}

## F. Hipótesis a contrastar

Para cada una, busca activamente evidencia a favor Y en contra, y concluye: apoyada, refutada o evidencia insuficiente. No la confirmes solo porque aparezca aquí.

{{hipotesis}}
{{bloque_iteracion}}
## G. Alcance

Incluye:
{{incluye}}

No incluye (no lo investigues en esta fase):
{{excluye}}

## H. Método y fuentes

{{metodo}}

Reglas que se aplican a todo el informe:
1. Prioriza fuentes primarias, oficiales y locales; si usas secundarias, dilo. Cada dato importante lleva fuente y fecha de consulta.
2. Etiqueta las afirmaciones relevantes: [HECHO], [ESTIMACIÓN], [INFERENCIA], [HIPÓTESIS], [RECOMENDACIÓN]. Una estimación nunca se presenta como dato; muestra el cálculo y los supuestos.
3. Si dos fuentes se contradicen, no elijas la favorable: compara calidad, actualidad, metodología y proximidad al mercado, y explica cuál se sostiene mejor.
4. Cada recomendación indica qué problema resuelve, qué evidencia la justifica, qué hipótesis valida y con qué métrica se sabrá si funciona. "Es una práctica habitual" no es un argumento.
5. Prioriza por impacto en el objetivo de negocio, coste, esfuerzo, velocidad y confianza, teniendo en cuenta las capacidades reales descritas en la sección C.
6. Si algo de la sección D resulta ser incorrecto, dilo en la sección "Cambios" con la evidencia.

## I. Formato de entrega

Markdown puro, compatible con Obsidian:
- Sin HTML, sin diagramas Mermaid, sin emojis decorativos.
- Cita en el texto con [n] y pon la lista completa en "Fuentes" con título, URL escrita entera y fecha de consulta. Las citas automáticas de la interfaz no siempre sobreviven a la descarga del informe: si una URL no está escrita en la sección Fuentes, para nosotros no existe.
- Tablas Markdown normales.

Estructura obligatoria (respeta títulos y orden). El resumen ejecutivo va al final a propósito: escríbelo después de todo el análisis, como síntesis de lo que hayan mostrado las secciones 1–7, sin anticipar conclusiones ni añadir nada que no esté en ellas.

# {{FXX}} — {{titulo_fase}}
## 1. Respuestas a las preguntas
(una subsección por pregunta Q1…Qn: respuesta, evidencia clave con [n], confianza alta/media/baja)
## 2. Evidencias y análisis
## 3. Hipótesis evaluadas
(tabla: ID | resultado | evidencia a favor | evidencia en contra | confianza)
## 4. Cambios respecto a lo que ya sabíamos
(qué conclusiones o datos de la sección D se refuerzan, debilitan o invalidan, citando su ID)
## 5. Implicaciones y recomendaciones
(cada una: problema → hipótesis → acción → métrica → prioridad P0/P1/P2)
## 6. Limitaciones y lo que no sabemos
## 7. Nuevas preguntas e hipótesis
## 8. Resumen ejecutivo
(máx. 15 líneas: respuesta directa a la pregunta principal y nivel de confianza global, coherente con las secciones 1–7)
## 9. Fuentes

## J. Control de calidad antes de entregar

Antes de terminar, revisa tu propio informe y corrige lo que falle:
- ¿Todo el análisis trata del objeto de la sección B?
- ¿El resumen ejecutivo (sección 8) dice lo mismo que las secciones 1–7, con la misma confianza?
- ¿Has respondido a todas las preguntas de la sección E, aunque sea con "no hay evidencia suficiente"?
- ¿Hay cifras sin fuente o estimaciones presentadas como hechos?
- ¿Cuadran las cifras y cálculos entre secciones?
- ¿Alguna recomendación contradice la sección C (capacidad, precios, restricciones) o la D.3 sin justificarlo?
- ¿Has buscado evidencia contra cada hipótesis?
- ¿Están todas las URLs escritas en la sección Fuentes?
````

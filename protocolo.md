---
tipo: protocolo
fecha_actualizacion: 2026-10-08
tags: [sistema, protocolo]
---

# Protocolo de investigación por fases

Este protocolo es **genérico**: vale para cualquier investigación de `investigaciones/`. Lo específico de cada una (objeto, negocio, restricciones del promotor, principios propios) vive en su `00_proyecto/01-contexto.md`. El formato de los archivos está en [convenciones](convenciones.md).

## Reparto de papeles

| Papel | Quién | Qué hace |
|---|---|---|
| **Gestor del protocolo** | Claude Code | Mantiene la memoria (registros, estado), prepara cada fase, genera el prompt autocontenido, audita el informe recibido y consolida lo aceptado. |
| **Investigador** | ChatGPT Deep Research (u otro) | Ejecuta **una** iteración de **una** fase a partir de un prompt que contiene todo el contexto que necesita. No tiene memoria entre conversaciones y no debe necesitarla. |
| **Decisor** | El promotor | Acepta o rechaza decisiones (`propuesta` → `adoptada`), aporta datos internos que no se pueden buscar fuera y decide qué fase sigue. |

**La memoria del proyecto vive en los archivos, nunca en una conversación.** Cada conversación con el investigador empieza de cero con un único prompt.

## Ciclo de una fase

```text
ficha de fase ──► /crear-prompt ──► prompt FXX-iNN ──► (ChatGPT) ──► informe FXX-iNN
                                                                           │
                       ┌───────────────────── /ingerir-informe ◄───────────┘
                       ▼
               revisión FXX-iNN (veredicto)
                       │
          ┌────────────┴─────────────┐
     rechazado / parcial          aceptado(-parcial)
          │                           │
   nueva iteración              /consolidar-fase
   (/crear-prompt ...            ├─ síntesis de la fase
    --iteracion)                 ├─ conclusiones / hipótesis / decisiones / preguntas / datos
                                 └─ 02-estado.md (avance + bitácora)
```

Una **fase** es una pregunta de investigación grande (p. ej. "demanda y perfiles de cliente"). Una **iteración** es un intento concreto de responderla: inicial, ampliación de un hueco, repetición tras un informe rechazado o verificación de datos. Una fase puede necesitar varias iteraciones; solo lo **consolidado** pasa a la memoria del proyecto.

## Reglas metodológicas

Estas reglas van, resumidas, dentro de cada prompt, y son también los criterios con los que se revisa cada informe.

1. **Objeto explícito.** Cada fase empieza definiendo qué se investiga exactamente y su relación con el negocio. Un informe que analiza otro mercado, otro producto o un caso "genérico" se rechaza entero, no se corrige.
2. **Jerarquía de evidencia.** Priorizar fuentes primarias, oficiales y locales. Si no existen, usar secundarias fiables y dejar constancia de la limitación. Cada dato importante lleva fuente (con URL escrita) y fecha de consulta.
3. **Hecho ≠ estimación ≠ inferencia ≠ hipótesis ≠ recomendación.** Cada afirmación relevante se etiqueta. Una estimación nunca se presenta como dato.
4. **"No lo sabemos" es un resultado válido.** Mejor 20 hechos bien verificados que 100 recopilados superficialmente. No se rellenan huecos con cifras inventadas.
5. **Buscar activamente evidencia contraria.** Las hipótesis heredadas y las del promotor se intentan refutar, no confirmar.
6. **Contradicciones.** Cuando dos fuentes chocan no se elige la favorable: se compara calidad, actualidad, metodología y proximidad al mercado, y se explica cuál se sostiene mejor.
7. **Acción ↔ hipótesis ↔ métrica.** Ninguna recomendación sin el problema que resuelve, la evidencia que la justifica y cómo se medirá. "Es una práctica habitual" no es un argumento.
8. **Priorización.** Impacto en el objetivo de negocio, coste, esfuerzo, velocidad para obtener resultado y confianza en la evidencia, teniendo en cuenta las capacidades reales del promotor.
9. **Definición de éxito.** Métricas de negocio por encima de las intermedias; las intermedias solo sirven para explicar las de negocio.
10. **Conclusiones provisionales y trazables.** Si una fase contradice o modifica una conclusión anterior, se dice explícitamente qué cambia y qué evidencia lo provoca. Nada se borra: cambia de estado.
11. **No reinvestigar lo consolidado** salvo que la fase sea precisamente de verificación o que haya evidencia nueva que lo cuestione.
12. **Formato como requisito técnico.** Markdown puro y portable (Obsidian): sin HTML, sin marcadores de cita de la interfaz, enlaces `[texto](url)` escritos, tablas Markdown normales.

## Criterios de revisión de un informe

`/ingerir-informe` puntúa cada criterio de 0 a 2 (0 = falla, 1 = parcial, 2 = cumple):

| # | Criterio | Pregunta |
|---|---|---|
| R1 | Fidelidad al objeto | ¿Investiga exactamente el objeto de la ficha, sin derivar a un caso genérico? |
| R2 | Cobertura | ¿Responde a cada pregunta de la ficha? (se detalla pregunta a pregunta) |
| R3 | Uso del contexto heredado | ¿Parte de lo consolidado sin contradecirlo sin justificación ni reinvestigarlo? |
| R4 | Calidad de fuentes | ¿Fuentes primarias/locales, con URL y fecha? ¿Cuántas afirmaciones clave quedan sin fuente? |
| R5 | Separación de evidencia | ¿Distingue hecho / estimación / inferencia / hipótesis / recomendación? |
| R6 | Evidencia contraria | ¿Intenta refutar las hipótesis que se le pasan? |
| R7 | Coherencia interna | ¿Cuadran cifras, cálculos y afirmaciones entre secciones? |
| R8 | Coherencia con la realidad del negocio | ¿Respeta precios, capacidad, restricciones y decisiones reales? |
| R9 | Accionabilidad | ¿Las recomendaciones están ligadas a hipótesis y métricas? |
| R10 | Formato | ¿Markdown limpio y estructura pedida? |

**Veredicto:**

- **aceptado**: ≥ 16/20 y ningún 0 en R1, R2 o R3.
- **aceptado-parcial**: 10–15, o ≥ 16 con algún 0 fuera de R1–R3. Se consolida solo lo que pasa la revisión y se abren preguntas/iteraciones para lo demás.
- **rechazado**: < 10, o un 0 en R1. No se consolida nada salvo, como mucho, hipótesis o preguntas útiles marcadas como tales.

El veredicto es una propuesta de Claude Code: el promotor puede cambiarlo.

## Quién ejecuta cada iteración

No todo tiene que ir a ChatGPT. La ficha de fase indica el `ejecutor` recomendado:

- `chatgpt-deep-research`: investigación externa amplia (mercado, competencia, demanda, canales).
- `claude-code`: análisis de activos propios con acceso al código, datos o analítica (p. ej. una auditoría técnica de la web propia) o verificaciones puntuales.
- `promotor`: datos internos que solo tiene el negocio (reservas reales, Keyword Planner, GBP).

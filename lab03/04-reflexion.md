---
documento: Reflexión
lab: 3
componente: C11 - API Generar Cuento
entregable: 4
---

# Entregable 4 — Reflexión

## ¿Qué funcionó bien en el prompt inicial?
- Dar **tipo, lenguaje y framework** explícitos (Servicio · Python · FastAPI) hizo que la
  estructura saliera correcta a la primera: endpoint, modelo de respuesta y forma general.
- Pegar la **especificación del Lab 2 tal cual** (propósito, entradas, salidas, flujo) evitó
  que la IA inventara el contrato de datos: `StoryResponse` salió alineado con el cliente.

## ¿Qué tuve que mejorar?
- Las **reglas medibles** hay que escribirlas como condiciones verificables, no como frases
  generales. "Tamaño máximo 5 MB" no basta; funcionó cuando dije *"si supera 5 MB → 400 con
  este mensaje exacto"*. Lo mismo con el timeout (→ 504) y con la privacidad (→ `del` en `finally`).
- Los **RNF** son los que más se olvidan: la primera versión abrió CORS a `*` y no descartaba
  el dibujo. Hubo que nombrarlos explícitamente como requisitos, no como deseos.
- Para que hubiera **pruebas reales**, tuve que pedir un diseño *testeable*: inyectar el
  pipeline y la configuración como dependencias. Sin eso, los tests habrían llamado a los
  servicios de IA y no serían unitarios ni rápidos.

## ¿Qué aprendí sobre cómo guiar a la IA para programar?
- **La especificación es el prompt.** Cuanto más medible es la spec, mejor es el código; el
  criterio de aceptación en formato *Dado/Cuando/Entonces* se traduce casi 1:1 en una prueba.
- **Iterar contra criterios, no contra impresiones.** Validar la v1 con una tabla de
  criterios (pasa/falla) convirtió "mejóralo" en instrucciones concretas y trazables.
- **La IA construye; el criterio no se delega.** La IA generó el andamiaje rápido, pero las
  decisiones de seguridad y de diseño (privacidad del dibujo, CORS, testabilidad) las tuve que
  fijar yo. Coincide con la idea de *vibe coding*: el agente ejecuta, el estudiante pone la vara.
- **Pedir el diseño para pruebas desde el prompt** ahorra una iteración entera: si el código
  nace con inyección de dependencias, las pruebas salen limpias y sin tocar servicios reales.

## Estado final de los criterios de aceptación

| Criterio | Estado |
|----------|--------|
| CA-1 · Archivo > 5 MB → 400 | ✅ (test `test_imagen_demasiado_grande_devuelve_400`) |
| CA-2 · Pipeline lento → 504 | ✅ (test `test_pipeline_lento_devuelve_504`) |
| CA-3 · Petición válida → 200 con 3 páginas | ✅ (test `test_peticion_valida_devuelve_3_paginas`) |
| RNF · Privacidad del dibujo (HU-05) | ✅ (`del image_bytes` en `finally`) |
| RNF · CORS restringido | ✅ (lista de orígenes desde configuración) |
| RNF · Errores sin filtrar detalles internos | ✅ (test `test_fallo_pipeline_devuelve_500`) |

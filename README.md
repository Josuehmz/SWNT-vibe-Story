# Laboratorio 3 — Implementación de Componentes con Vibe Coding (StoryDraw)

> **Materia:** Desarrollo asistido por IA (vibe coding)
> **Aplicación:** StoryDraw — convierte el dibujo de un niño en un cuento ilustrado y narrado.
> **Componente implementado:** **C11 · API Generar Cuento** (Servicio, módulo M5).

## ➡️ Entrega actual: Lab 3 → carpeta [`lab03/`](lab03/)

Ciclo completo de vibe coding sobre un componente crítico: **especificación → prompt inicial →
código → validación contra criterios → prompt refinado → código final probado → reflexión.**
Escrito en Markdown estructurado (frontmatter YAML, tablas de trazabilidad, criterios
*Dado/Cuando/Entonces*) para que **tanto una persona como una IA** lo lean y califiquen sin ambigüedad.

### 📂 Entregables del Lab 3

| Entregable | Archivo |
|-----------|---------|
| **1. Prompt inicial** usado en Vibe Coding | [`lab03/01-prompt-inicial.md`](lab03/01-prompt-inicial.md) |
| **2. Código generado + validación** (v1 con huecos → tabla criterios pasa/falla) | [`lab03/02-codigo-generado.md`](lab03/02-codigo-generado.md) |
| **3. Prompt refinado** (cada mejora trazada al hueco que corrige) | [`lab03/03-prompt-refinado.md`](lab03/03-prompt-refinado.md) |
| **4. Reflexión** (qué funcionó, qué mejoré, qué aprendí) | [`lab03/04-reflexion.md`](lab03/04-reflexion.md) |
| **Código final ejecutable + pruebas** (`pytest` → 7 passed) | [`lab03/codigo/`](lab03/codigo/) |

### 🧭 Cómo leer/calificar el Lab 3 (guía para el evaluador o la IA)

1. **Prompt inicial** (`01`): verificar que traduce la especificación del componente (propósito,
   entradas/salidas, reglas, RNF, criterios) a un prompt técnico completo.
2. **Validación de la v1** (`02`): tabla que marca cada criterio de aceptación y RNF como
   pasa/falla, justificando los huecos del código generado con el prompt inicial.
3. **Prompt refinado** (`03`): cada mejora está trazada al hueco que corrige (tabla *mejora → hueco*).
4. **Código final** (`lab03/codigo/`): `main.py` (FastAPI) + `test_main.py` con **una prueba por
   criterio de aceptación**. Ejecutar `pytest -q` debe dar `7 passed`.
5. **Reflexión** (`04`): responde las tres preguntas del lab y cierra el estado de los criterios.

### ✔️ Estado de los criterios de aceptación de C11
Todos verificados con pruebas unitarias ([`lab03/codigo/test_main.py`](lab03/codigo/test_main.py)):
archivo > 5 MB → 400 · tipo no permitido → 400 · imagen vacía → 400 · petición válida → 200 con
3 páginas · pipeline lento → 504 · fallo del pipeline → 500 sin filtrar detalles · privacidad del
dibujo (`del` en `finally`) · CORS restringido.

---

## Antecedente: Lab 2 — Especificaciones de la App

El Lab 3 parte de la especificación producida en el Lab 2. Esos entregables viven en la **raíz de
este repositorio** y son el insumo directo del prompt del Lab 3:

| Archivo | Contenido |
|---------|-----------|
| [`00-insumos-semana1.md`](00-insumos-semana1.md) | Problema, público, propuesta de valor e historias de usuario (HU-01…HU-06). |
| [`01-mapa-de-componentes.md`](01-mapa-de-componentes.md) | Mapa de Componentes v1: 6 módulos, 17 componentes, dependencias (Mermaid), MVP vs. futuro. |
| [`02-especificaciones/`](02-especificaciones/) | 6 especificaciones de componentes críticos. **La de C11** ([`C11-api-generar-cuento.md`](02-especificaciones/C11-api-generar-cuento.md)) es la que implementa el Lab 3. |
| [`03-trazabilidad.md`](03-trazabilidad.md) | Matriz HU → componentes → criterios de aceptación. |

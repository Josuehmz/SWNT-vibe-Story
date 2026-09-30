# Laboratorio 3 — Implementación de Componentes con Vibe Coding

> **Materia:** Desarrollo asistido por IA (vibe coding) · **App:** StoryDraw
> **Componente implementado:** C11 · API Generar Cuento (Servicio, módulo M5).

Ciclo completo de vibe coding sobre un componente crítico del Lab 2: especificación → prompt
inicial → código → validación contra criterios → prompt refinado → código final probado → reflexión.

## 📂 Estructura y entregables

| Archivo | Entregable del Lab 3 |
|---------|----------------------|
| [`01-prompt-inicial.md`](01-prompt-inicial.md) | **1.** Prompt inicial usado en Vibe Coding |
| [`02-codigo-generado.md`](02-codigo-generado.md) | **2.** Código generado (v1 con huecos + validación) + enlace al final |
| [`03-prompt-refinado.md`](03-prompt-refinado.md) | **3.** Prompt refinado con mejoras (trazado a cada hueco) |
| [`04-reflexion.md`](04-reflexion.md) | **4.** Reflexión (qué funcionó, qué mejoré, qué aprendí) |
| [`codigo/`](codigo/) | Código final ejecutable + pruebas (`pytest` → 7 passed) |

## ✔️ Estado de los criterios de aceptación (C11)
Todos verificados con pruebas unitarias en [`codigo/test_main.py`](codigo/test_main.py):
archivo > 5 MB → 400 · tipo no permitido → 400 · imagen vacía → 400 · petición válida → 200 con
3 páginas · pipeline lento → 504 · fallo del pipeline → 500 sin filtrar detalles · privacidad
del dibujo (`del` en `finally`) · CORS restringido.

## Origen de la especificación
La spec del componente está en el Lab 2: [`../02-especificaciones/C11-api-generar-cuento.md`](../02-especificaciones/C11-api-generar-cuento.md).

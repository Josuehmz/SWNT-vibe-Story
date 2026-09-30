# Laboratorio 2 — Especificaciones de la App (StoryDraw)

> **Materia:** Desarrollo asistido por IA (vibe coding)
> **Aplicación:** StoryDraw — convierte el dibujo de un niño en un cuento ilustrado y narrado.
> **Entregable:** Mapa de Componentes v1 + Especificaciones de componentes críticos.

Este repositorio contiene **únicamente** el entregable del Laboratorio 2. Está escrito en
Markdown estructurado (encabezados consistentes, frontmatter YAML, tablas y un diagrama
Mermaid) para que **tanto una persona como una IA** puedan leerlo y calificarlo sin ambigüedad.

## 📂 Estructura

| Archivo | Contenido | Entregable / Rúbrica |
|---------|-----------|----------------------|
| [`00-insumos-semana1.md`](00-insumos-semana1.md) | Problema, público, propuesta de valor e historias de usuario (HU-01…HU-06). | Requisito previo |
| [`01-mapa-de-componentes.md`](01-mapa-de-componentes.md) | Mapa de Componentes v1: módulos, componentes, dependencias (Mermaid), MVP vs. futuro. | **Entregable 1** · Rúbrica "Mapa de Componentes" (30 pts) |
| [`02-especificaciones/`](02-especificaciones/) | 6 especificaciones de componentes críticos (una por archivo). | **Entregable 2** · Rúbrica "Especificaciones funcionales" (30) + "RNF y criterios" (25) |
| [`03-trazabilidad.md`](03-trazabilidad.md) | Matriz HU → componentes → criterios de aceptación. | Rúbrica "Presentación y consistencia" (15) |

## 🧭 Cómo leer/calificar este entregable (guía para el evaluador o la IA)

1. **Mapa de Componentes** (`01-…`): verificar que hay 3–6 módulos, 2–5 componentes por módulo,
   cada uno clasificado (UI/Servicio/Datos/Integración) y con dependencias explícitas.
2. **Especificaciones** (`02-…`): cada archivo sigue la plantilla oficial (Propósito, Entradas,
   Salidas, Reglas de negocio, Flujo principal ≤ 5 pasos, RNF, Criterios de aceptación en
   formato *Dado/Cuando/Entonces*). El frontmatter YAML declara `id`, `tipo`, `historias`.
3. **Trazabilidad** (`03-…`): confirmar que **cada HU está cubierta por ≥ 1 componente** y que
   cada componente tiene criterios de aceptación verificables.

## 🗺️ Índice de componentes

| ID | Componente | Tipo | Módulo | HU |
|----|-----------|------|--------|----|
| C01 | Lienzo de Dibujo | UI | M1 | HU-01 |
| C04 | Caso de Uso Generar Cuento | Servicio | M2 | HU-02, HU-04, HU-05, HU-06 |
| C11 | API Generar Cuento | Servicio | M5 | HU-02, HU-05 |
| C12 | Pipeline de IA | Servicio | M5 | HU-02, HU-03, HU-05 |
| C10 | Almacenamiento Local | Datos | M4 | HU-04, HU-06 |
| C07 | Visor de Cuento con Narración | UI | M3 | HU-03, HU-04 |

## 📊 Rúbrica de evaluación (100 pts)

| Criterio | Peso | Dónde se evidencia |
|----------|------|--------------------|
| Mapa de Componentes | 30 | `01-mapa-de-componentes.md` |
| Especificaciones funcionales | 30 | `02-especificaciones/*` (Propósito, E/S, reglas) |
| RNF + Criterios de aceptación | 25 | `02-especificaciones/*` (RNF + Dado/Cuando/Entonces) |
| Presentación y consistencia | 15 | `03-trazabilidad.md` + formato uniforme |

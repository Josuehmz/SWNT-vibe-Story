---
documento: Matriz de Trazabilidad
app: StoryDraw
---

# Matriz de Trazabilidad — HU → Componentes → Criterios

Cada historia de usuario está cubierta por al menos un componente crítico con criterios de
aceptación verificables.

## HU → Componentes

| HU | Descripción breve | Componentes que la cubren |
|----|-------------------|---------------------------|
| HU-01 | Dibujar libremente | C01 (Lienzo), C02 (Herramientas), C03 (Exportador) |
| HU-02 | Generar cuento con un botón | C04 (Caso de Uso), C06 (Cliente HTTP), C11 (API), C12 (Pipeline) |
| HU-03 | Narración en voz alta | C16 (Voz TTS), C08 (Audio), C07 (Visor) |
| HU-04 | Volver a ver los cuentos | C09 (Galería), C10 (Almacenamiento Local), C07 (Visor) |
| HU-05 | Privacidad del dibujo | C04 (guarda solo local), C11 (no persiste), C12 (descarta el dibujo) |
| HU-06 | Límite de 3 cuentos gratuitos | C10 (contador + bandera de límite) |

## Componente → HU → Criterio de aceptación clave

| Componente | HU | Criterio verificable |
|-----------|----|----------------------|
| C01 Lienzo | HU-01 | Sin trazos, el botón "crear cuento" está deshabilitado. |
| C04 Caso de Uso | HU-02, HU-04, HU-05, HU-06 | Éxito → guarda cuento y +1 al contador; fallo → sin cambios. |
| C11 API | HU-02, HU-05 | Valida ≤ 5 MB; responde 3 páginas; no persiste el dibujo. |
| C12 Pipeline | HU-02, HU-03, HU-05 | Devuelve 3 páginas; degrada a placeholder / sin audio sin romperse. |
| C10 Almacenamiento Local | HU-04, HU-06 | Poda a 20 cuentos; `hasReachedFreeLimit=true` con 3 cuentos. |
| C07 Visor + Narración | HU-03, HU-04 | Reproduce narración; sin audio no muestra control roto. |

## Cobertura

- **HU cubiertas:** 6 / 6 (HU-01 … HU-06).
- **HU sin cubrir:** ninguna.
- **Componentes críticos especificados:** 6 (C01, C04, C07, C10, C11, C12).
